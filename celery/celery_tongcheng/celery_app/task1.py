# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import time
import uuid

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
def token_fetch(self):
    token = 'https://openserviceauth.ctrip.com/openserviceauth/authorize.ashx?AID={0}&SID={1}&KEY={2}'.format(
        AID, SID, TOKEN_KEY)
    token_result = requests.post(token)
    Refresh_Token = token_result.json()['Refresh_Token']

    Atoken = 'https://openserviceauth.ctrip.com/openserviceauth/refresh.ashx?AID={0}&SID={1}&refresh_token={2}'.format(
        AID, SID, Refresh_Token)
    Atoken_result = requests.post(Atoken)
    Access_Token = Atoken_result.json()['Access_Token']

    self.rdb.hset('xiecheng_token', 'access_token', Access_Token)
    self.rdb.hset('xiecheng_token', 'expire_time',
                  datetime.datetime.now() + datetime.timedelta(seconds=600))
    print('xiecheng_access_token update is OK!')
    return ['xiecheng_access_token update is OK!']


@app.task(base=XiechengTask, ignore_result=True, max_retries=3)
def citys_fetch():
    with open(r"/home/fanjindong/notebook/celery/celery_demo/celery_app/携程国内城市.xml") as f:
        data = f.read()

    data_json = xmltodict.parse(data)
    items = data_json['CityDetails']['CityDetail']
    for item in items:
        city = int(item['City'])
        hotel_ids_fetch.delay(city)  # async
    return ['citys is OVER!']


# 查询酒店全量ID列表
@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def hotel_ids_fetch(self, city, page_index=1):
    """查询酒店全量ID列表"""
    Access_Token = self.rdb.hget('xiecheng_token', 'access_token')
    #expire_time = self.rdb.hget('xiecheng_token', 'expire_time')
    # if (not Access_Token) or str(datetime.datetime.now())>expire_time:
    #     token_fetch.delay()
    #     hotel_ids_fetch.delay(city,page_index)
    #     return ['Access_Token is expire so hotel_ids_fetch is retries']
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
    except KeyError as e:
        token_fetch()
        hotel_ids_fetch.apply_async(args=[city, page_index], countdown=60)
        return['city', city, 'EOFError']

    if page_index * 5000 < total:
        page_index += 1
        hotel_ids_fetch.apply_async(args=[city, page_index])

    for hotel_id in hotel_ids:
        hotel_message_fetch.delay(hotel_id)  # async
    return [city, page_index, len(hotel_ids), 'is over']


# ## 酒店静态信息查询

@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def hotel_message_fetch(self, hotel_id, try_number=1):
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
                   '<HotelDescriptiveInfo HotelCode="{4}" PositionTypeCode="502">'
                   '<HotelInfo SendData="true"/>'
                   '<FacilityInfo SendGuestRooms="true"/>'
                   '<AreaInfo SendAttractions="true" SendRecreations="true"/>'
                   '<ContactInfo SendData="true"/>'
                   '<MultimediaObjects SendData="true"/>'
                   '</HotelDescriptiveInfo>'
                   '</HotelDescriptiveInfos>'
                   '</OTA_HotelDescriptiveInfoRQ>'
                   '</RequestBody>'
                   '</HotelRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>').format(AID, SID, ts, sign, hotel_id)

    encode_xml = request_xml.encode('utf-8')

    headers = {'Content-Type': 'text/xml; charset=utf-8',
               'Host': 'openapi.ctrip.com', 'Content-Length': len(encode_xml)}
    resp = requests.post(url=ping_url, data=encode_xml, headers=headers).text
    xmlt_data = xmltodict.parse(xmltodict.parse(resp)[
        'soap:Envelope']['soap:Body']['RequestResponse']['RequestResult'])
    # xml 转 dict
    xmlt_data = (json.loads(
        (json.dumps(xmlt_data, ensure_ascii=False, indent=2)).replace('@', '')))
    # dict 拆解 并去除’@‘
    dirty_datas = {}
    clean_datas = {}
    room_datas = {}

    def dict_open(self):
        """dict拆分"""
        if isinstance(self, dict):
            for key in self.keys():
                value = self[key]
                dirty_datas[key] = value
                dict_open(value)
        if isinstance(self, list):
            for item in self:
                dict_open(item)
    # 调用dict拆分function并赋值给dirty_datas
    dict_open(xmlt_data)

    def judgment(keys, data=dirty_datas, default=[]):
        try:
            if isinstance(keys, str):
                return data.get(keys, default)
            if isinstance(keys, list):
                if not len(keys) == 1:
                    if judgment(keys[0], data=data):
                        return judgment(keys[1:], data=judgment(keys[0], data=data))
                else:
                    return judgment(keys[-1], data=data)
        except KeyError as e:
            return []

    clean_datas['id'] = judgment('HotelCode')

    if (not clean_datas['id'])and try_number <= 3:
        # 酒店ID查询为空，重新查询（最大重试次数为3）
        hotel_message_fetch.apply_async(
            (hotel_id, try_number + 1), countdown=30)
        return [hotel_id, 'message retries', try_number, '30s']
    elif (not clean_datas['id'])and try_number > 3:
        # 酒店ID查询为空，重试次数超过3次，忽略之.
        return [hotel_id, 'message not found']
    elif (not judgment('GuestRoom'))and clean_datas['id']:
        # 酒店ID非空，rooms字段为空，判断为下线酒店，执行数据库删除操作
        self.mdb['jiudian_hotels'].delete_many({'id': clean_datas['id']})
        return [clean_datas['id'], 'delete basedata is over']

    clean_datas['name'] = judgment('HotelName')
    clean_datas['brandCode'] = judgment('BrandCode')
    clean_datas['cityCode'] = judgment('HotelCityCode')
    clean_datas['areaId'] = judgment('AreaID')

    items = judgment('Service')
    if not isinstance(items, list):
        items = [items]
    clean_datas['services'] = []
    for item in items:
        clean_datas['services'].append(judgment('Code', data=item))

    items = judgment('ThemeCategoryType')
    if not isinstance(items, list):
        items = [items]
    clean_datas['themes'] = []
    for item in items:
        if judgment('Code', data=item):
            clean_datas['themes'].append(judgment('Code', data=item))

    clean_datas['images'] = []
    items = judgment('ImageItem')
    if not isinstance(items, list):
        items = [items]
    for item in items:
        clean_datas['images'].append({
            'category': judgment('Category', data=item),
            'caption': judgment(["Description", 'Caption'], data=item),
            'url': judgment(["ImageFormat", 'URL'], data=item)
        })

    clean_datas['phones'] = []
    items = judgment('Phone')
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if judgment('PhoneNumber', data=item):
            clean_datas['phones'].append(item['PhoneNumber'])

    clean_datas['descriptions'] = []
    items = judgment('TextItem')
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if item.get('Category') and item.get('Description'):
            clean_datas['descriptions'].append(
                {'category': item['Category'], 'content': item['Description']})
    clean_datas['address'] = judgment('Address')
    clean_datas['lat'] = judgment('Latitude')
    clean_datas['lng'] = judgment('Longitude')
    clean_datas['lng'] = [clean_datas['lng'], clean_datas['lat']]
    clean_datas['categoryCodes'] = judgment(['SegmentCategory', 'Code'])
    clean_datas['isOnlineFranchise'] = judgment('IsOnlineFranchise')
    clean_datas['lastUpdated'] = judgment('LastUpdated')
    if judgment('WhenBuilt'):
        clean_datas['whenBuilt'] = judgment('WhenBuilt')
    dl = []
    items = judgment(['Policy', 'PolicyInfoCodes',
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
            "CheckOutTime": judgment(['Policy', 'PolicyInfo', 'CheckOutTime']),
            "CheckInTime": judgment(['Policy', 'PolicyInfo', 'CheckInTime'])
        },
        "PolicyInfoCodes": {
            "PolicyInfoCode": {
                "Description": dl,
                "Code": judgment(['Policy', 'PolicyInfoCodes', 'PolicyInfoCode', 'Code'])
            }
        }
    }
    clean_datas['refPoints'] = judgment('RefPoint')
    clean_datas['awards'] = {}
    items = judgment('Award')
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if judgment('Provider', data=item):
            clean_datas['awards'][judgment('Provider', data=item)] = judgment(
                'Rating', data=item)
    clean_datas['tpa_Extensions'] = {
        "MasterSubHotelIDs": judgment('MasterSubHotelIDs'),
        "Roomquantity": judgment('Roomquantity'),
        "CityImportantMessage": judgment('CityImportantMessage'),
        "ThemeCategory": judgment('ThemeCategory')
    }

    # room
    rooms = judgment('GuestRoom')
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
        room_datas['tpa_Extensions'] = clean_datas['tpa_Extensions']
        rooms_list.append(room_datas)
    clean_datas['rooms'] = rooms_list
    # rooms 字段为rooms_list 完成
    self.mdb['jiudian_hotels'].update_one({'id': clean_datas['id']},
                                          {'$set': clean_datas},
                                          upsert=True)
    hotel_price.delay(hotel_id)  # async
    # print('>>>', clean_datas['id'], 'message is over')
    return [clean_datas['id'], 'message is over']


# price 查询
@app.task(base=XiechengTask, bind=True, ignore_result=True, max_retries=3)
def hotel_price(self, hotel_id, try_number=1):
    """酒店ID对应最低价price查询"""
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
                   '<ns:OTA_HotelRatePlanRQ TimeStamp="{7}" Version="1.0">'
                   '<ns:RatePlans>'
                   '<ns:RatePlan>'
                   '<ns:DateRange Start="{4}" End="{5}"/>'
                   '<ns:RatePlanCandidates>'
                   '<ns:RatePlanCandidate AvailRatesOnlyInd="true" IsCNYCurrency="true" RatePlanCode=" " >'
                   '<ns:HotelRefs>'
                   '<ns:HotelRef HotelCode="{6}"/>'
                   '</ns:HotelRefs>'
                   '</ns:RatePlanCandidate>'
                   '</ns:RatePlanCandidates>'
                   '<ns:TPA_Extensions RestrictedDisplayIndicator="false" />'
                   '</ns:RatePlan>'
                   '</ns:RatePlans>'
                   '</ns:OTA_HotelRatePlanRQ>'
                   '</RequestBody>'
                   '</HotelRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>').format(
                       AID, SID, ts, sign, start, end, hotel_id, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+08:00'))
    encode_xml = request_xml.encode('utf-8')
    headers = {'Content-Type': 'text/xml; charset=utf-8',
               'Host': 'openapi.ctrip.com', 'Content-Length': len(encode_xml)}
    resp = requests.post(url=ping_url, data=encode_xml, headers=headers).text
    xmlt_data = xmltodict.parse(xmltodict.parse(resp)[
        'soap:Envelope']['soap:Body']['RequestResponse']['RequestResult'])
    # xml 转 dict
    xmlt_data = (json.loads(
        (json.dumps(xmlt_data, ensure_ascii=False, indent=2)).replace('@', '')))

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
    hotelid = judgment(['Response', 'HotelResponse',
                        'OTA_HotelRatePlanRS', 'RatePlans', 'HotelCode'])
    if (not hotelid)and try_number <= 3:
        # print('>>>',hotel_id,'retries')
        hotel_price.apply_async((hotel_id, try_number + 1), countdown=30)
        # print('>>>', hotel_id, 'prices retries', try_number, '30s')
        return ['>>>', hotel_id, 'prices retries', try_number, '30s']
    elif (not hotelid)and try_number > 3:
        # print('>>>', hotel_id, 'prices not found')
        return ['>>>', hotel_id, 'prices not found']
    items = judgment(['Response', 'HotelResponse',
                      'OTA_HotelRatePlanRS', 'RatePlans', 'RatePlan'])

    def price(items):
        """遍历并拿到最小price"""
        prices = []
        if not items:
            return -1
        else:
            for item in items:
                item = judgment(['Rates', 'Rate'], data=item)
                if not item:
                    return -1
                else:

                    for ite in item:
                        price = judgment(
                            ['BaseByGuestAmts', 'BaseByGuestAmt', 'AmountBeforeTax'],
                            data=ite,
                            default=-1
                        )
                        try:
                            prices.append(int(float(price)))
                        except Exception as e:
                            pass
        if prices:
            return min(prices)
        else:
            return -1
    price = price(items)

    self.mdb['jiudian_hotels'].update_one(
        {'id': str(hotel_id)},
        {'$set': {'price': price}},
        upsert=True
    )
    # print('>>>', hotelid, price, 'price is over')
    return [hotelid, price, 'price is over']


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
    end = datetime.datetime.now() - datetime.timedelta(minutes=10)
    end = end.strftime("%Y-%m-%dT%H:%M:%S")
    start = datetime.datetime.now() - datetime.timedelta(hours=5)
    start = start.strftime("%Y-%m-%dT%H:%M:%S")

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
        page_index += 1
        get_hotel_info_increment.delay(city_id, page_index)
        # print(city_id, hotel_ids)
        for hotel_id in hotel_ids:
            hotel_message_fetch.delay(hotel_id)  # async
        return['city', city_id, 'page_index', page_index - 1, 'updating']
    else:
        return ['city', city_id, 'update increment is over']
