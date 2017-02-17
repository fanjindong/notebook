
# coding: utf-8

# ## import

# In[1]:

import time
import hashlib
import requests
import xmltodict
import json
import uuid
import re
import datetime
import hashlib
import requests
import json
import pymongo
from pymongo import MongoClient
import logging
import threading
import time

import progressbar
client = MongoClient('mongodb://localhost:27017')
db = client.test
hotel = db.jiudian_hotels
room = db.jiudian_room

AID = 328727
SID = 810129
UUID = uuid.uuid1()
ICODE = 'e6fb53910a134cdd96fc4ba30f864c7d'
API_URL = 'openapi.ctrip.com'
KEY = 'E0F33944-A048-45F7-AA91-A55196051B91'
TOKEN_KEY = 'f017b34784be441780a8cc79ccd4a9ed'
type(UUID)


# ## 查询酒店全量ID列表
def hotel_ids_fetch():
    page_index = 1
    ids = []
    while page_index:
        token = 'https://openserviceauth.ctrip.com/openserviceauth/authorize.ashx?AID={0}&SID={1}&KEY={2}'.format(
            AID, SID, TOKEN_KEY)
        token_result = requests.post(token)
        Refresh_Token = token_result.json()['Refresh_Token']

        Atoken = 'https://openserviceauth.ctrip.com/openserviceauth/refresh.ashx?AID={0}&SID={1}&refresh_token={2}'.format(
            AID, SID, Refresh_Token)
        Atoken_result = requests.post(Atoken)
        Access_Token = Atoken_result.json()['Access_Token']

        url_html = 'http://openservice.ctrip.com/OpenService/ServiceProxy.ashx?AID={0}&SID={1}&ICODE={2}&UUID={3}&Token={4}&mode=1&format=json'.format(
            AID, SID, ICODE, UUID, Access_Token)
        data = {
            "City": 1,
            "PageIndex": str(page_index),
            "PageSize": "5000"
        }

        requests_result = requests.post(url_html, data=data)
    #     print(json.dumps(requests_result.json(),indent=4))
        hotel_ids = requests_result.json()['HotelIDs'].split(',')
        total = requests_result.json()['Total']
        ids.extend(hotel_ids)
        if page_index * 5000 < total:
            page_index += 1
        else:
            page_index = 0
    return ids


# price 查询
def hotel_price(hotel_id):
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
                   '</soap:Envelope>').format(AID, SID, ts, sign, start, end, hotel_id, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+08:00'))
    encode_xml = request_xml.encode('utf-8')
    headers = {'Content-Type': 'text/xml; charset=utf-8',
               'Host': 'openapi.ctrip.com', 'Content-Length': len(encode_xml)}
    resp = requests.post(url=ping_url, data=encode_xml, headers=headers).text
    xmlt_data = xmltodict.parse(xmltodict.parse(resp)['soap:Envelope'][
                                'soap:Body']['RequestResponse']['RequestResult'])
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
    items = judgment(['Response', 'HotelResponse',
                      'OTA_HotelRatePlanRS', 'RatePlans', 'RatePlan'])

    def price(items):
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
                            ['BaseByGuestAmts', 'BaseByGuestAmt', 'AmountBeforeTax'], data=ite, default=-1)
                        try:
                            prices.append(int(float(price)))
                        except Exception as e:
                            pass
        if prices:
            return min(prices)
        else:
            return -1
    price = price(items)
    # hotel.update_one({'id': str(hotel_id)}, {
    #                  '$set': {'price': price}}, upsert=True)
    # print(hotel_id, 'price', price)
    return price

# ## 酒店静态信息查询


def hotel_message_fetch(hotel_id):
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
    xmlt_data = xmltodict.parse(xmltodict.parse(resp)['soap:Envelope'][
                                'soap:Body']['RequestResponse']['RequestResult'])
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
        room.update_one({'roomTypeCode': room_datas['roomTypeCode']},
                        {'$set': room_datas}, upsert=True)
        rooms_list.append(room_datas)
    price = hotel_price(hotel_id)
    clean_datas['rooms'] = rooms_list
    clean_datas['price'] = price
    hotel.update_one({'id': clean_datas['id']},
                     {'$set': clean_datas},
                     upsert=True)
    print('>>>', clean_datas['id'], price, 'over')
    # return [clean_datas['id'], room_datas['roomTypeCode']]


def update_hotel():
    """更新酒店上下线静态数据
    """
    new_ids = hotel_ids_fetch()
    old_ids = []
    for old_id in hotel.find({}, {'id': 1, '_id': 0}):
        if isinstance(old_id['id'], str):
            old_ids.append((old_id['id']))
    on_ids = []
    off_ids = []
    # 上线ID
    for new_id in new_ids:
        if not new_id in old_ids:
            on_ids.append(new_id)
    # 更新上线酒店数据
    for on_id in on_ids:
        hotel_message_fetch(int(on_id))

    # 下线ID
    for old_id in old_ids:
        if not old_id in new_ids:
            off_ids.append(old_id)
    # 删除下线酒店数据
    for off_id in off_ids:
        hotel.delete_many({'id': off_id})


@app.task
def xiecheng_start():
    hotel_ids = hotel_ids_fetch()
    for hotel_id in hotel_ids:
        hotel_message_fetch(int(hotel_id))
