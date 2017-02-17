# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import hashlib
import json
import logging
import time
import uuid
from pprint import pprint

import redis
import requests
import xmltodict
from celery import Task
from pymongo import MongoClient

from celery_app import app

AID = 328727
SID = 810129
UUID = uuid.uuid1()
ICODE = 'e6fb53910a134cdd96fc4ba30f864c7d'
API_URL = 'openapi.ctrip.com'
KEY = 'E0F33944-A048-45F7-AA91-A55196051B91'
TOKEN_KEY = 'f017b34784be441780a8cc79ccd4a9ed'


class XiechengTask(Task):
    abstract = True
    _mdb = None
    _rdb = None

    @property
    def mdb(self):
        if self._mdb is None:
            _mc = MongoClient('mongodb://localhost:27017')
            self._mdb = _mc["test"]
        return self._mdb

    @property
    def rdb(self):
        if self._rdb is None:
            self._rdb = redis.StrictRedis(host='127.0.0.1',
                                          port='6379',
                                          db=0)
        return self._rdb


@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def token_fetch_and_update(self):
    """获取、更新携程access token,存储于radis中,失效后可再次获取
    """
    try:
        token = 'https://openserviceauth.ctrip.com/openserviceauth/authorize.ashx?AID={0}&SID={1}&KEY={2}'.format(
            AID, SID, TOKEN_KEY)
        token_result = requests.post(token)
        Refresh_Token = token_result.json()['Refresh_Token']

        Atoken = 'https://openserviceauth.ctrip.com/openserviceauth/refresh.ashx?AID={0}&SID={1}&refresh_token={2}'.format(
            AID, SID, Refresh_Token)
        Atoken_result = requests.post(Atoken)
        Access_Token = Atoken_result.json()['Access_Token']
    except KeyError:
        return ['token_fetch_and_update retry']

    self.rdb.hset('xiecheng_token', 'access_token', Access_Token)
    self.rdb.hset('xiecheng_token', 'expire_time',
                  datetime.datetime.now() + datetime.timedelta(seconds=60 * 9))
    print('xiecheng_access_token update is OK!')
    return ['xiecheng_access_token update is OK!']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def full_citys_fetch():
    with open(r"/home/fanjindong/notebook/celery/celery_demo/celery_app/携程国内城市.xml") as f:
        data = f.read()

    data_json = xmltodict.parse(data)
    items = data_json['CityDetails']['CityDetail']
    for item in items:
        city = int(item['City'])
        city_get_full_hotel_ids.delay(city)  # async
    return ['citys is OVER!']


# 查询酒店全量ID列表
@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def city_get_full_hotel_ids(self, city, page_index=1):
    """根据城市ID，查询酒店全量ID列表，并调用静态信息接口
    """
    Access_Token = self.rdb.hget(
        'xiecheng_token', 'access_token').decode('UTF-8')
    url_html = 'http://openservice.ctrip.com/OpenService/ServiceProxy.ashx?AID={0}&SID={1}&ICODE={2}&UUID={3}&Token={4}&mode=1&format=json'.format(
        AID, SID, ICODE, UUID, Access_Token)
    data = {
        "City": city,
        "PageIndex": str(page_index),
        "PageSize": "5000"
    }

    try:
        requests_result = requests.post(url_html, data=data)
        resp_data = requests_result.json()
        total = resp_data['Total']
        if int(total) == 0:
            return ['city', city, 'total 0']
        hotel_ids = resp_data['HotelIDs'].split(',')
    except Exception as e:  # Keyerro
        if str(datetime.datetime.now()) > (self.rdb.hget(
                'xiecheng_token', 'expire_time')).decode('UTF-8'):
            token_fetch_and_update()
        city_get_full_hotel_ids.apply_async(args=[city, page_index])
        return['city', city, 'EOFError']

    if page_index * 5000 < total:
        city_get_full_hotel_ids.apply_async(args=[city, page_index + 1])

    for hotel_ids_index in range(len(hotel_ids) // 10 + 1):
        hotel_ids_message_fetch.delay(
            hotel_ids[hotel_ids_index * 10:(hotel_ids_index + 1) * 10])  # async
    return [city, page_index, len(hotel_ids), 'is over']


@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def datas_purge_and_insert(self, dirty_datas):
    """数据清洗、插入数据库
    """
    # dirty_datas = {}  # 存放爬取接口所返回的初始数据
    clean_datas = {}  # 存放经映射后的静态信息数据
    room_datas = {}  # 存放经映射后的酒店房型数据集

    def judgment(keys, data=None, default=None):
        """ 传入keys=[key1,key2,key3],
            执行data[key1][key2][key3],
            防止报错，若获取失败则返回[] or None
        """
        if data is None:
            data = dirty_datas
        try:
            if isinstance(keys, str):
                return data[keys]
            elif isinstance(keys, list):
                if len(keys) == 1:
                    return data[keys[0]]
                else:
                    return judgment(keys[1:], data=data[keys[0]])
            else:
                return default
        except (KeyError, AttributeError, TypeError) as e:
            return default
    # 映射数据结构
    clean_datas['id'] = judgment('HotelCode')
    clean_datas['name'] = judgment('HotelName')
    clean_datas['brandCode'] = judgment('BrandCode')
    clean_datas['cityCode'] = judgment('HotelCityCode')
    clean_datas['areaId'] = judgment('AreaID')

    items = judgment(['HotelInfo', 'Services', 'Service'])
    if not isinstance(items, list):
        items = [items]
    clean_datas['services'] = []
    for item in items:
        clean_datas['services'].append(judgment('Code', data=item))

    items = judgment(['TPA_Extensions', 'ThemeCategory', 'ThemeCategoryType'])
    if not isinstance(items, list):
        items = [items]
    clean_datas['themes'] = []
    for item in items:
        if judgment('Code', data=item):
            clean_datas['themes'].append(judgment('Code', data=item))
    # 'images','descriptions'字段在一个list中，故放在一起处理
    clean_datas['images'] = []
    clean_datas['descriptions'] = []
    items_desc = judgment(['MultimediaDescriptions', 'MultimediaDescription'])
    if items_desc:
        try:
            items = judgment(['ImageItems', 'ImageItem'], data=items_desc[0])
        except KeyError as e:
            # 如果报错，说明image 和textitem 字段两者缺一或都不存在
            items = judgment(['ImageItems', 'ImageItem'], data=items_desc)
        if not isinstance(items, list):
            items = [items]
        for item in items:
            clean_datas['images'].append({
                'category': judgment('Category', data=item),
                'caption': judgment(["Description", 'Caption'], data=item),
                'url': judgment(["ImageFormat", 'URL'], data=item)
            })
        try:
            items = judgment(['TextItems', 'TextItem'], data=items_desc[1])
        except KeyError as e:
            items = judgment(['TextItems', 'TextItem'], data=items_desc)
        if not isinstance(items, list):
            items = [items]
        for item in items:
            if item.get('Category') and item.get('Description'):
                clean_datas['descriptions'].append(
                    {'category': item['Category'], 'content': item['Description']})

    clean_datas['phones'] = []
    items = judgment(['ContactInfos', 'ContactInfo', 'Phones', 'Phone'])
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if judgment('PhoneNumber', data=item):
            clean_datas['phones'].append(item['PhoneNumber'])

    clean_datas['address'] = judgment(['HotelInfo', 'Address'])
    clean_datas['lat'] = judgment(['HotelInfo', 'Position', 'Latitude'])
    clean_datas['lng'] = judgment(['HotelInfo', 'Position', 'Longitude'])
    clean_datas['loc'] = [clean_datas['lng'], clean_datas['lat']]

    clean_datas['categoryCodes'] = {
        "SegmentCategory": judgment(
            ['HotelInfo', 'CategoryCodes', 'SegmentCategory', 'Code']
        )
    }
    clean_datas['isOnlineFranchise'] = judgment(
        ['HotelInfo', 'IsOnlineFranchise'])
    clean_datas['lastUpdated'] = judgment(['HotelInfo', 'LastUpdated'])
    if judgment('WhenBuilt'):
        clean_datas['whenBuilt'] = judgment(['HotelInfo', 'WhenBuilt'])
    dl = []
    items = judgment(['Policies', 'Policy', 'PolicyInfoCodes',
                      'PolicyInfoCode', 'Description'])
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if isinstance(item, dict):
            if item.get('Text') and item.get('Name'):
                dl.append({'Text': judgment('Text', item),
                           'Name': judgment('Name', item)})
    clean_datas['policies'] = {
        "PolicyInfo": {
            "CheckOutTime": judgment(
                ['Policies', 'Policy', 'PolicyInfo', 'CheckOutTime']),
            "CheckInTime": judgment(
                ['Policies', 'Policy', 'PolicyInfo', 'CheckInTime'])
        },
        "PolicyInfoCodes": {
            "PolicyInfoCode": {
                "Description": dl,
                "Code": judgment(
                    ['Policies', 'Policy',
                     'PolicyInfoCodes', 'PolicyInfoCode', 'Code'])
            }
        }
    }
    clean_datas['refPoints'] = judgment(['AreaInfo', 'RefPoints', 'RefPoint'])
    clean_datas['awards'] = {}
    items = judgment(['AffiliationInfo', 'Awards', 'Award'])
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if judgment('Provider', data=item):
            clean_datas['awards'][judgment('Provider', data=item)] = judgment(
                'Rating', data=item)
    clean_datas['tpa_Extensions'] = judgment('TPA_Extensions')

    # room
    rooms = judgment(['FacilityInfo', 'GuestRooms', 'GuestRoom'])
    rooms_list = []
    if not isinstance(rooms, list):
        rooms = [rooms]
    for item in rooms:
        room_datas['hotelId'] = judgment('HotelCode')
        room_datas['roomName'] = judgment(['RoomTypeName'], data=item)
        room_datas['roomTypeCode'] = judgment(
            ['TypeRoom', 'RoomTypeCode'], data=item)
        room_datas['standardOccupancy'] = judgment(
            ['TypeRoom', 'StandardOccupancy'], data=item)
        room_datas['nameSort'] = judgment(['TypeRoom', 'Name'], data=item)
        room_datas['floor'] = judgment(['TypeRoom', 'Floor'], data=item)
        room_datas['invBlockCode'] = judgment(
            ['TypeRoom', 'InvBlockCode'], data=item)
        room_datas['nonSmoking'] = judgment(
            ['TypeRoom', 'NonSmoking'], data=item)
        room_datas['hasWindow'] = judgment(
            ['TypeRoom', 'HasWindow'], data=item)
        room_datas['quantity'] = judgment(['TypeRoom', 'Quantity'], data=item)
        room_datas['roomSize'] = judgment(['TypeRoom', 'RoomSize'], data=item)
        room_datas['bedSize'] = judgment(['TypeRoom', 'Size'], data=item)
        room_datas['bedType'] = judgment(
            ['TypeRoom', 'BedTypeCode'], data=item)
        room_datas['HID'] = judgment(['TypeRoom', 'HID'], data=item)
        if judgment('Amenities', data=item):
            room_datas['amentities'] = judgment(
                ['Amenities', 'Amenity'], data=item)
        room_datas['tpa_Extensions'] = judgment(
            ['TPA_Extensions', 'TPA_Extension'], data=item)
        rooms_list.append(room_datas)
    clean_datas['rooms'] = rooms_list  # rooms 字段为rooms_list 完成
    clean_datas = {k: v for k, v in clean_datas.items() if v}
    self.mdb['jiudian_hotels'].update_one(
        {'id': clean_datas['id']}, {'$set': clean_datas}, upsert=True)
    return [clean_datas['id'], 'message insert Ok']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def hotel_ids_message_fetch(hotel_ids):
    """酒店静态信息查询"""
    ping_url = 'http://{}/Hotel/OTA_HotelDescriptiveInfo.asmx'.format(API_URL)
    ts = int(time.time())
    secret = hashlib.md5(KEY.encode('utf8')).hexdigest().upper()
    sign = hashlib.md5('{0}{1}{2}{3}OTA_Ping'.format(
        ts, AID, secret, SID).encode('utf-8')).hexdigest().upper()
    request_xml = ('<?xml version="1.0" encoding="utf-8"?>'
                   '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
                   '<soap:Body>'
                   '<Request xmlns="http://ctrip.com/">'
                   '<requestXML><![CDATA['
                   '<?xml version="1.0" encoding="utf-8"?>'
                   '<Request>'
                   '<Header AllianceID="{0}" SID="{1}" TimeStamp="{2}" RequestType="OTA_Ping" Signature="{3}" />'
                   '<HotelRequest>'
                   '<RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
                   '<OTA_HotelDescriptiveInfoRQ Version="1.0" xsi:schemaLocation="http://www.opentravel.org/OTA/2003/05OTA_HotelDescriptiveInfoRQ.xsd" xmlns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                   '<HotelDescriptiveInfos>'
                   "{4}"
                   '</HotelDescriptiveInfos>'
                   '</OTA_HotelDescriptiveInfoRQ>'
                   '</RequestBody>'
                   '</HotelRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>')
    hotel_desc = ('<HotelDescriptiveInfo HotelCode="{0[index]}" PositionTypeCode="502">'
                  '<HotelInfo SendData="true"/>'
                  '<FacilityInfo SendGuestRooms="true"/>'
                  '<AreaInfo SendAttractions="true" SendRecreations="true"/>'
                  '<ContactInfo SendData="true"/>'
                  '<MultimediaObjects SendData="true"/>'
                  '</HotelDescriptiveInfo>')
    hotel_index = ''
    n = len(hotel_ids)
    if n == 0:
        return ['hotel_ids is []']
    for i in range(n):
        hotel_index += hotel_desc.replace('index', str(i))
    hotel_desc = hotel_index.format(hotel_ids)
    request_xml = request_xml.format(AID, SID, ts, sign, hotel_desc)
    # pprint(request_xml)
    encode_xml = request_xml.encode('utf-8')

    headers = {'Content-Type': 'text/xml; charset=utf-8',
               'Host': 'openapi.ctrip.com', 'Content-Length': len(encode_xml)}
    try:
        resp = requests.post(url=ping_url, data=encode_xml,
                             headers=headers).text
        xmlt_data = xmltodict.parse(xmltodict.parse(resp)[
            'soap:Envelope']['soap:Body']['RequestResponse']['RequestResult'])
        # xml 转 dict
        xmlt_data = (json.loads(
            (json.dumps(xmlt_data, ensure_ascii=False, indent=2)).replace('@', '')))
        datas = xmlt_data['Response']['HotelResponse']['OTA_HotelDescriptiveInfoRS'][
            'HotelDescriptiveContents']['HotelDescriptiveContent']
    except KeyError as e:
        hotel_ids_message_fetch.delay(hotel_ids)
        pprint(hotel_ids)
        return ['hotel_ids_message_fetch retries']
    if not isinstance(datas, list):
        datas = [datas]
    for data in datas:
        datas_purge_and_insert.delay(data)
    hotel_ids_rateplans_fetch.delay(hotel_ids)
    return ['message fetch is OK']


# price 查询

@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def rateplans_get_price_and_insert(self, rateplans_data):
    """传入价格日历列表，计算最低价price字段的值，并插入数据库
    """
    def judgment(keys, data=None, default=None):
        """ 传入keys=[key1,key2,key3],
            执行data[key1][key2][key3],
            防止报错，若获取失败则返回[] or None
        """
        if data is None:
            data = rateplans_data
        try:
            if isinstance(keys, str):
                return data[keys]
            elif isinstance(keys, list):
                if len(keys) == 1:
                    return data[keys[0]]
                else:
                    return judgment(keys[1:], data=data[keys[0]])
            else:
                return default
        except (KeyError, AttributeError, TypeError) as e:
            return default
    try:
        hotel_id = rateplans_data['HotelCode']
        items = rateplans_data['RatePlan']
    except KeyError:
        return [rateplans_data.get('HotelCode'), 'RatePlans no data']

    def to_price(items):
        """遍历并拿到最小price
        """
        prices = {}
        if not items:
            return -1
        if not isinstance(items, list):
            items = [items]
        for item in items:
            item = judgment(['Rates', 'Rate'], data=item)
            if not item:
                return -1
            for ite in item:
                amount = judgment(
                    ['BaseByGuestAmts', 'BaseByGuestAmt'],
                    data=ite
                )
                if amount:
                    key = (float(amount['AmountBeforeTax']))
                    value = (float(amount['ListPrice']))
                    prices[key] = value
    # 将价格price和门市价listprice作为键值对存入字典prices中
        if prices:
            price = min(list(prices.keys()))
            listprice = prices[price]
            return price, listprice
        else:
            return -1, -1
    # try:
    #     price, listprice = to_price(items)
    # except TypeError:
    #     print(items)
    price, listprice = to_price(items)
    if price != -1:
        self.mdb['jiudian_hotels'].update_one(
            {'id': hotel_id},
            {'$set': {'price': price, 'ListPrice': listprice}},
            upsert=True  # 参数设置为Fal，还未修改
        )
    return [hotel_id, price, 'price insert OK']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def hotel_ids_rateplans_fetch(hotel_ids):
    """查询酒店ID对应price日历，返回最低价格
    """
    start = str(datetime.date.today())
    end = str(datetime.date.today() + datetime.timedelta(days=28))
    ping_url = 'http://{}/Hotel/OTA_HotelRatePlan.asmx'.format(API_URL)
    ts = int(time.time())
    secret = hashlib.md5(KEY.encode('utf8')).hexdigest().upper()
    sign = hashlib.md5('{0}{1}{2}{3}OTA_HotelRatePlan'.format(
        ts, AID, secret, SID).encode('utf-8')).hexdigest().upper()

    request_xml = ('<?xml version="1.0" encoding="utf-8"?>'
                   '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
                   '<soap:Body>'
                   '<Request xmlns="http://ctrip.com/">'
                   '<requestXML><![CDATA['
                   '<?xml version="1.0" encoding="utf-8"?>'
                   '<Request>'
                   '<Header AllianceID="{0}" SID="{1}" TimeStamp="{2}" RequestType="OTA_HotelRatePlan" Signature="{3}"/>'
                   '<HotelRequest>'
                   '<RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
                   '<ns:OTA_HotelRatePlanRQ TimeStamp="{4}" Version="1.0">'
                   '<ns:RatePlans>'
                   "{rateplans}"
                   '</ns:RatePlans>'
                   '</ns:OTA_HotelRatePlanRQ>'
                   '</RequestBody>'
                   '</HotelRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>')
    rateplan = ('<ns:RatePlan>'
                '<ns:DateRange Start="{start}" End="{end}"/>'
                '<ns:RatePlanCandidates>'
                '<ns:RatePlanCandidate AvailRatesOnlyInd="true" IsCNYCurrency="true" RatePlanCode=" " >'
                '<ns:HotelRefs>'
                '<ns:HotelRef HotelCode="{hotel_ids[index]}"/>'
                '</ns:HotelRefs>'
                '</ns:RatePlanCandidate>'
                '</ns:RatePlanCandidates>'
                '<ns:TPA_Extensions RestrictedDisplayIndicator="false" />'
                '</ns:RatePlan>')
    rateplans = ''
    n = len(hotel_ids)
    for index in range(n):
        rateplans += rateplan.replace('index', str(index))
    rateplans = rateplans.format(hotel_ids=hotel_ids, start=start, end=end)
    request_xml = request_xml.format(
        AID, SID, ts, sign, datetime.datetime.now(
        ).strftime('%Y-%m-%dT%H:%M:%S.%f+08:00'), rateplans=rateplans)
    encode_xml = request_xml.encode('utf-8')
    headers = {'Content-Type': 'text/xml; charset=utf-8',
               'Host': 'openapi.ctrip.com', 'Content-Length': len(encode_xml)}
    try:
        resp = requests.post(url=ping_url, data=encode_xml,
                             headers=headers).text
        xmlt_data = xmltodict.parse(xmltodict.parse(resp)[
            'soap:Envelope']['soap:Body']['RequestResponse']['RequestResult'])
        # xml 转 dict
        xmlt_data = (json.loads(
            (json.dumps(xmlt_data, ensure_ascii=False, indent=2)).replace('@', '')))
        datas = xmlt_data['Response']['HotelResponse'][
            'OTA_HotelRatePlanRS']['RatePlans']
    except KeyError:
        hotel_ids_rateplans_fetch.delay(hotel_ids)
        return ['hotel_ids_rateplans_fetch retry']
    if isinstance(datas, list):
        for data in datas:
            rateplans_get_price_and_insert.delay(data)
    else:
        rateplans_get_price_and_insert.delay(datas)
    return ['rateplans fetch is OK']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def update_hotel():
    """更新上下线酒店增量信息"""
    with open(r"/home/fanjindong/notebook/celery/celery_demo/celery_app/携程国内城市.xml") as f:
        data = f.read()
    data_json = xmltodict.parse(data)
    items = data_json['CityDetails']['CityDetail']
    for item in items:
        city = int(item['City'])
        get_hotel_info_increment.delay(city)  # async
    return ['update_hotel function is OVER!']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def get_hotel_info_increment(city_id, page_index=1):
    """查询city所属酒店增量ID信息，并调用静态信息查询接口"""
    ping_url = 'http://{}/hotel/GetHotelInfoIncrement.asmx'.format(API_URL)
    ts = int(time.time())
    end = datetime.datetime.now() - datetime.timedelta(minutes=1)
    end = end.strftime("%Y-%m-%dT%H:%M:%S")
    start = datetime.datetime.now() - datetime.timedelta(minutes=16)
    start = start.strftime("%Y-%m-%dT%H:%M:%S")
    # start-end 时间间隔15分钟
    secret = hashlib.md5(KEY.encode('utf8')).hexdigest().upper()
    sign = hashlib.md5('{0}{1}{2}{3}GetHotelInfoIncrement'.format(
        ts, AID, secret, SID).encode('utf-8')).hexdigest().upper()

    request_xml = ('<?xml version="1.0" encoding="utf-8"?>'
                   '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
                   '<soap:Body>'
                   '<Request xmlns="http://ctrip.com/">'
                   '<requestXML><![CDATA['
                   '<?xml version="1.0" encoding="utf-8"?>'
                   '<Request>'
                   '<Header AllianceID="{0}" SID="{1}" TimeStamp="{2}" RequestType="GetHotelInfoIncrement" Signature="{3}" />'
                   '<GetHotelInfoIncrementRequest>'
                   '<StartTime>{4}</StartTime>'
                   '<EndTime>{5}</EndTime>'
                   '<CityID>{6}</CityID>'
                   '<PageSize>10</PageSize>'
                   '<PageIndex>{7}</PageIndex>'
                   '<CountryID>1</CountryID>'
                   '</GetHotelInfoIncrementRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>').format(AID, SID, ts, sign, start, end, city_id, page_index)

    encode_xml = request_xml.encode('utf-8')

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Host': 'openapi.ctrip.com',
        'Content-Length': len(encode_xml)
    }
    resp = requests.post(url=ping_url, data=encode_xml, headers=headers).text
    xmlt_data = xmltodict.parse(xmltodict.parse(resp)['soap:Envelope'][
        'soap:Body']['RequestResponse']['RequestResult'])
    # xml 转 dict
    xmlt_data = (json.loads(
        (json.dumps(xmlt_data, ensure_ascii=False, indent=2)).replace('@', '')))

    # 代码健壮性之首要！
    def judgment(keys, data=xmlt_data, default=[]):
        try:
            if isinstance(keys, str)and isinstance(data, dict):
                return data.get(keys, default)
            if isinstance(keys, list)and isinstance(data, dict):
                if not len(keys) == 1:
                    if judgment(keys[0], data=data):
                        return judgment(keys[1:], data=judgment(keys[0], data=data))
                else:
                    return judgment(keys[-1], data=data)
            else:
                return []
        except KeyError as e:
            return []
    access_count = judgment(['Response', 'Header', 'AccessCount'])
    hotel_ids = judgment(
        ['Response', 'GetHotelInfoIncrementResponse', 'HotelInfoChangeList', 'HotelID'])
    if hotel_ids:
        if not isinstance(hotel_ids, list):
            hotel_ids = [hotel_ids]
        get_hotel_info_increment.delay(city_id, page_index + 1)

        for hotel_ids_index in range(len(hotel_ids) // 10 + 1):
            hotel_ids_message_fetch.delay(
                hotel_ids[hotel_ids_index * 10:(hotel_ids_index + 1) * 10])

        return['city', city_id, page_index, 'updating']
    else:
        return ['city', city_id, page_index, 'updating']
