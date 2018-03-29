# coding:utf-8
import uuid
PRO_MONGO_HOST = ["mongodb://root:Boluome123@192.168.1.6", "192.168.1.7"]
STG_MONGO_HOST = ["mongodb://root:Boluome123@192.168.2.3", "192.168.2.4"]
DEV_MONGO_HOST = ["mongodb://root:Boluome123@192.168.0.7", "192.168.0.10"]
CTRIP_MONGO_HOST = ["mongodb://root:Boluome123@192.168.0.14"]
STATIC_MONGO_HOST = ["mongodb://root:Boluome123@192.168.1.21", "192.168.1.22"]

REPLICASET_NAME = 'foba'

DEV_REDIS_MAST_HOST = '192.168.0.11'
DEV_REDIS_PAYM_HOST = '192.168.0.3'
DEV_REDIS_NEW_HOST = '192.168.0.6'
STG_REDIS_MAST_HOST = '192.168.2.6'
STG_REDIS_NEW_HOST = '192.168.2.6'
PRO_REDIS_MAST_HOST = '192.168.1.9'
PRO_REDIS_PAYM_HOST = '192.168.1.11'
PRO_REDIS_ACTIVITY_HOST = '192.168.1.14'

PRO_REDIS_HOST = '192.168.1.9'
STG_REDIS_HOST = '192.168.2.6'
DEV_REDIS_HOST = '192.168.0.11'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_DB_0 = 0
REDIS_DB_1 = 1
REDIS_DB_2 = 2
REDIS_DB_4 = 4
REDIS_DB_7 = 7

REDIS_ACTIVITY_HOST = '192.168.2.6'
REDIS_PAYMENT_HOST = '192.168.0.3'
REDIS_ACTIVITY_PORT = 6379
REDIS_ACTIVITY_DB = 0
REDIS_ACTIVITY_SCRATCH_DB = 3

PG_BOLUOME = "host=192.168.0.8 dbname=boluome user=boluome password=Boluome123"
DEV_PG_ACCOUNT = "host=192.168.0.8 dbname=account user=root password=Boluome123"
STG_PG_ACCOUNT = "host=192.168.2.10 dbname=account user=root password=Boluome123"
PRO_PG_ACCOUNT = "host=192.168.1.13 dbname=account user=root password=Boluome123"

TONGCHENG_AGENT_ACCOUNT = 'd79bd00d-ca25-4167-96b8-31c4a25778e1'
TONGCHENG_APP_KEY = '126e7e38-ef8c-427f-8387-90202c9721e4'
TONGCHENG_API_SERVER = 'http://www.lvcang.cn/jingqu/Services/'

SPIDER_SERVER = 'http://filmapi.spider.com.cn/v2/boluomi/'
SPIDER_APP_KEY = 'boluomi'
SPIDER_APP_SECRET = 'BV07RK5W9U3Z'

KOMOVIE_SERVER = 'http://api.komovie.cn/movie/service'
KOMOVIE_CHANNEL_ID = '189'
KOMOVIE_MD5_KEY = 'GglrL3WIjp6CUZnj'

# 测试
TEST_YIGUO_HOST = 'https://t007208.yiguo.com/YGOpenAPI/values'
TEST_YIGUO_CUSTOME_CODE = 'blm123456'
TEST_YIGUO_BIZ_SOURCE = 'yiguo'
# 正式
YIGUO_HOST = 'https://ygopen.yiguo.com/YGOpenAPI/values'
YIGUO_CUSTOME_CODE = 'T-BLM'
YIGUO_BIZ_SOURCE = '3941A7D740F6474B907BFBDC50B1E2CF'

YONGLE_UNIONID = 62485393


XIECHENG_AID = 328727
XIECHENG_SID = 810129
XIECHENG_UUID = uuid.uuid1()
XIECHENG_ICODE = 'e6fb53910a134cdd96fc4ba30f864c7d'
XIECHENG_API_URL = 'openapi.ctrip.com'
XIECHENG_KEY = 'E0F33944-A048-45F7-AA91-A55196051B91'
XIECHENG_TOKEN_KEY = 'f017b34784be441780a8cc79ccd4a9ed'

XIECHENG_TOKEN_URL = 'https://openserviceauth.ctrip.com/openserviceauth/'

XIECHENG_POST_URL = 'http://openservice.ctrip.com/OpenService/ServiceProxy.ashx?AID={0}&SID={1}&ICODE={2}&UUID={3}&Token={4}&mode=1&format=json'

MQ_BROKER = 'amqp://blm:Blm123@localhost:5672//'
# MQ_BROKER = "amqp://blm:Blm123@192.168.2.8:5672//"

MQ_ZHENLV = "dpp_zhenlv_tasks"
MQ_QUNAR = "dpp_qunar_tasks"
MQ_QUNAR_JIPIAO = "dpp_qunar_jipiao_tasks"
MQ_TONGCHENG = "dpp_tongcheng_tasks"
MQ_XIECHENG = "dpp_ctrip_tasks"
MQ_SPIDER = "dpp_spider_tasks"
MQ_KOMOVIE = "dpp_komovie_tasks"
MQ_SHARE_IMG = "dpp_share_img_tasks"
MQ_PG = "dpp_pg_sync_tasks"
MQ_LVMAMA = "dpp_lvmama_tasks"
MQ_REPORT = "dpp_report_tasks"
MQ_SETTLEMENT = "dpp_settlement_tasks"
MQ_PINGAN = "dpp_pingan_tasks"
MQ_YIGUO = "dpp_yiguo_tasks"
MQ_YONGLE = "dpp_yongle_tasks"
MQ_MAOYAN = "dpp_maoyan_tasks"
MQ_DEMO = "dpp_demo_tasks"

SUBMAIL_APPID = '11664'
SUBMAIL_APPKEY = '26a5a8c9fe31f28a60fa1f2558f9d8fd'
SUBMAIL_MAIL_URL = 'https://api.submail.cn/mail/xsend'
SUBMAIL_PROJECT = '1iyqA1'


QUNAR_APP_KEY = '10383738'
QUNAR_SECRET_KEY = 'jMrETuGb'
QUNAR_VERSION = '3.1.0'
QUNAR_QUERY_HOTEL_LIST_URL = 'http://api.hds.qunar.com/api/hotel/queryHotelList.json'
QUNAR_QUERY_HOTEL_DETAIL_URL = 'http://api.hds.qunar.com/api/hotel/queryHotelDetail.json'
QUNAR_QUERY_RATE_PLAN_URL = 'http://api.hds.qunar.com/api/hotel/queryRatePlan.json'
QUNAR_QUERY_HOTEL_INCREMENT_URL = 'http://api.hds.qunar.com/api/hotel/queryHotelIncrement.json'
QUNAR_QUERY_CHANGED_PRICE_URL = 'http://api.hds.qunar.com/api/hotel/queryChangedPrice.json'

ZHENLV_URL = "http://api.tdxinfo.com/service/flight/domestic"
ZHENLV_USER = "563716d245ced1d2ea3ffe61"
ZHENLV_SIGN_CODE = "3e62869b"
ZHENLV_RAW = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><TzRequest xmlns="http://www.travelzen.com/flight/base" xmlns:domestic="http://www.travelzen.com/flight/domestic" xmlns:insure="http://www.travelzen.com/flight/insure" xmlns:international="http://www.travelzen.com/flight/international" xmlns:basic="http://www.travelzen.com/flight/basic" ><requestMetaInfo><userName>{user}</userName><signCode>{sign}</signCode><timeStamp>{ts}</timeStamp><responseDataType>JSON</responseDataType></requestMetaInfo><requestEntity xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="domestic:FlightSearchV2Request"><domestic:flightRange><domestic:fromCity>{from_city}</domestic:fromCity><domestic:toCity>{to_city}</domestic:toCity><domestic:fromDate>{date}</domestic:fromDate></domestic:flightRange><domestic:lowestPrice>false</domestic:lowestPrice><domestic:openingTime>true</domestic:openingTime></requestEntity></TzRequest>'

CITY_MAP = {'HET': '呼和浩特', 'DLC': '大连', 'NNG': '南宁', 'CKG': '重庆', 'CSX': '长沙', 'SIA': '西安',
            'SHA': '上海', 'SYX': '三亚', 'KHN': '南昌', 'SZX': '深圳', 'CAN': '广州', 'KWE': '贵阳',
            'KMG': '昆明', 'XMN': '厦门', 'HFE': '合肥', 'CTU': '成都', 'TAO': '青岛', 'WUH': '武汉',
            'NKG': '南京', 'FOC': '福州', 'TNA': '济南', 'BJS': '北京', 'TSN': '天津', 'CGO': '郑州',
            'HRB': '哈尔滨', 'SHE': '沈阳', 'HGH': '杭州'}


SCRATCH_KEY = 'scratch:57e3507cea8a682600b1432e'
SCRATCH_ORDER_KEY = 'scratch_order'

INVITE_COUPON_URL = 'http://192.168.2.2:32800/api/v1/marketing/invite_coupon'

COUPON_URL = 'http://stg.web.boluomeet.com/coupon'

XIECHENG_AID = 328727
XIECHENG_SID = 810129
XIECHENG_UUID = uuid.uuid1()
XIECHENG_ICODE = 'e6fb53910a134cdd96fc4ba30f864c7d'
XIECHENG_API_URL = 'openapi.ctrip.com'
XIECHENG_KEY = 'E0F33944-A048-45F7-AA91-A55196051B91'
XIECHENG_TOKEN_KEY = 'f017b34784be441780a8cc79ccd4a9ed'
XIECHENG_TOKEN_URL = 'https://openserviceauth.ctrip.com/openserviceauth/'

XIECHENG_POST_URL = 'http://openservice.ctrip.com/OpenService/ServiceProxy.ashx?AID={0}&SID={1}&ICODE={2}&UUID={3}&Token={4}&mode=1&format=json'

XIECHENG_MESSAGE_XML = ('<?xml version="1.0" encoding="utf-8"?>'
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
XIECHENG_MESSAGE_DESC = ('<HotelDescriptiveInfo HotelCode="{0[index]}" PositionTypeCode="502">'
                         '<HotelInfo SendData="true"/>'
                         '<FacilityInfo SendGuestRooms="true"/>'
                         '<AreaInfo SendAttractions="true" SendRecreations="true"/>'
                         '<ContactInfo SendData="true"/>'
                         '<MultimediaObjects SendData="true"/>'
                         '</HotelDescriptiveInfo>')
XIECHENG_PRICE_XML = ('<?xml version="1.0" encoding="utf-8"?>'
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
XIECHENG_PRICE_RATEPLAN = ('<ns:RatePlan>'
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
XIECHENG_INCREMENT_XML = ('<?xml version="1.0" encoding="utf-8"?>'
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
                          '</soap:Envelope>')
CTRIP_AID = {'oklife': 698282, 'other': 328727}
CTRIP_SID = {'oklife': 1235859, 'other': 810129}
CTRIP_KEY = {'oklife': '8EEA26EC-F03F-41B0-A0FB-F7B15E0E840D', 'other': 'E0F33944-A048-45F7-AA91-A55196051B91'}
CTRIP_API_URL = 'openapi.ctrip.com'
CTRIP_ORDER_XML = ('<?xml version="1.0" encoding="utf-8"?>'
                   '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
                   '<soap:Body>'
                   '<Request xmlns="http://ctrip.com/">'
                   '<requestXML><![CDATA['
                   '<?xml version="1.0" encoding="utf-8"?>'
                   '<Request>'
                   '<Header AllianceID="{0}" SID="{1}" TimeStamp="{2}" RequestType=" D_HotelOrderMiniInfo" Signature="{3}" />'
                   '<HotelOrderMiniInfoRequest>'
                   '<AllianceId>{0}</AllianceId>'
                   '<Sid>{1}</Sid>'
                   '<OrderId>{4}</OrderId>'
                   '</HotelOrderMiniInfoRequest>'
                   '</Request>]]>'
                   '</requestXML>'
                   '</Request>'
                   '</soap:Body>'
                   '</soap:Envelope>')
