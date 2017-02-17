# coding:utf-8
import uuid
PRO_MONGO_HOST = ["mongodb://root:Boluome123@192.168.1.6", "192.168.1.7"]
STG_MONGO_HOST = ["mongodb://root:Boluome123@192.168.2.3", "192.168.2.4"]
DEV_MONGO_HOST = ["mongodb://root:Boluome123@192.168.0.7", "192.168.0.10"]

REPLICASET_NAME = 'foba'

PRO_REDIS_HOST = '192.168.1.9'
STG_REDIS_HOST = '192.168.2.5'
DEV_REDIS_HOST = '192.168.0.11'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_DB_7 = 7

REDIS_ACTIVITY_HOST = '192.168.2.5'
REDIS_ACTIVITY_PORT = 6379
REDIS_ACTIVITY_DB = 0
REDIS_ACTIVITY_SCRATCH_DB = 3

TONGCHENG_AGENT_ACCOUNT = 'd79bd00d-ca25-4167-96b8-31c4a25778e1'
TONGCHENG_APP_KEY = '126e7e38-ef8c-427f-8387-90202c9721e4'
TONGCHENG_API_SERVER = 'http://www.lvcang.cn/jingqu/Services/'

XIECHENG_AID = 328727
XIECHENG_SID = 810129
XIECHENG_UUID = uuid.uuid1()
XIECHENG_ICODE = 'e6fb53910a134cdd96fc4ba30f864c7d'
XIECHENG_API_URL = 'openapi.ctrip.com'
XIECHENG_KEY = 'E0F33944-A048-45F7-AA91-A55196051B91'
XIECHENG_TOKEN_KEY = 'f017b34784be441780a8cc79ccd4a9ed'

XIECHENG_TOKEN_URL = 'https://openserviceauth.ctrip.com/openserviceauth/authorize.ashx?AID={0}&SID={1}&KEY={2}'
XIECHENG_ATOKEN_URL = 'https://openserviceauth.ctrip.com/openserviceauth/refresh.ashx?AID={0}&SID={1}&refresh_token={2}'
XIECHENG_POST_URL = 'http://openservice.ctrip.com/OpenService/ServiceProxy.ashx?AID={0}&SID={1}&ICODE={2}&UUID={3}&Token={4}&mode=1&format=json'

XIECHENG_PRICE_URL = '<?xml version="1.0" encoding="utf-8"?>'
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
    '</soap:Envelope>'
XIECHENG_MESSAGE_URL = '<?xml version="1.0" encoding="utf-8"?>'
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
    '</soap:Envelope>'

MQ_BROKER = "amqp://blm:blm123@192.168.2.6//"

MQ_ZHENLV = "stg_zhenlv_tasks"
MQ_QUNAR = "stg_qunar_tasks"
MQ_QUNAR_JIPIAO = "stg_qunar_jipiao_tasks"
MQ_TONGCHENG = "stg_tongcheng_tasks"
MQ_XIECHENG = "stg_xiecheng_tasks"

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

ZHENLV_HOT_LINES = [
    'CAN-TSN', 'SHA-TNA', 'BJS-CGO', 'CAN-FOC', 'BJS-XMN', 'SHA-FOC', 'BJS-KHN', 'SZX-CKG',
    'CGO-CAN', 'KMG-SZX', 'TNA-SHA', 'CGO-SZX', 'CAN-TNA', 'SZX-TNA', 'CGO-BJS', 'NNG-SHA',
    'HGH-CAN', 'KMG-BJS', 'CAN-SYX', 'SIA-CAN', 'KMG-SHA', 'SHA-WUH', 'SHA-CGO', 'SZX-SHA', 'HFE-BJS',
    'XMN-BJS', 'SHA-NNG', 'SYX-CAN', 'BJS-TAO', 'SZX-TAO', 'DLC-SZX', 'SHA-CTU', 'FOC-SHA',
    'CAN-SIA', 'CAN-DLC', 'CAN-NKG', 'SHA-XMN', 'CAN-CGO', 'SIA-BJS', 'DLC-BJS', 'KMG-CTU', 'BJS-KMG',
    'CAN-XMN', 'BJS-WUH', 'TSN-CAN', 'NKG-SHA', 'SHA-TSN', 'SHA-CSX', 'FOC-SZX', 'SZX-CTU',
    'SZX-FOC', 'XMN-CAN', 'CSX-CAN', 'NKG-CAN', 'SHA-SZX', 'CAN-TAO', 'BJS-NKG', 'SIA-SZX', 'CSX-SZX',
    'CSX-BJS', 'BJS-SZX', 'SYX-BJS', 'SZX-CSX', 'BJS-CAN', 'SZX-HGH', 'SHA-SYX', 'CKG-CAN', 'SZX-XMN',
    'SHA-KMG', 'BJS-HET', 'BJS-CKG', 'TAO-BJS', 'HET-BJS', 'TNA-CAN', 'CTU-SZX', 'SHA-DLC', 'CAN-WUH',
    'CAN-BJS', 'SZX-DLC', 'XMN-SZX', 'KMG-CAN', 'WUH-SZX', 'BJS-TNA', 'FOC-CAN', 'SYX-SZX', 'SHE-BJS',
    'SHA-KWE', 'BJS-DLC', 'KWE-SHA', 'SYX-SHA', 'SHA-HRB', 'BJS-CSX', 'XMN-SHA', 'CAN-KMG', 'NKG-SZX',
    'CGO-SHA', 'WUH-CAN', 'CAN-CTU', 'SHA-SIA', 'CKG-SZX', 'TAO-SHA', 'CSX-SHA', 'TAO-SZX', 'SHA-CKG',
    'SIA-SHA', 'HGH-SZX', 'SZX-TSN', 'SZX-NKG', 'DLC-CAN', 'SHA-BJS', 'TNA-SZX', 'NKG-BJS', 'SZX-SIA',
    'HRB-SHA', 'HGH-BJS', 'CAN-HGH', 'DLC-SHA', 'SZX-KMG', 'BJS-CTU', 'FOC-BJS', 'CKG-BJS', 'TAO-CAN',
    'BJS-HGH', 'CTU-BJS', 'CAN-SHA', 'CAN-CSX', 'KHN-BJS', 'BJS-SYX', 'TNA-BJS', 'BJS-SHE', 'CTU-SHA',
    'BJS-SHA', 'SHA-NKG', 'CTU-KMG', 'SZX-CGO', 'CKG-SHA', 'WUH-BJS', 'SZX-SYX', 'TSN-SHA',
    'CTU-CAN', 'BJS-HFE', 'SHA-TAO', 'CAN-CKG', 'SHA-CAN', 'WUH-SHA', 'SZX-BJS', 'SZX-WUH', 'BJS-FOC',
    'TSN-SZX', 'BJS-SIA'
]
ZHENLV_CABIN = {
    "3UC": "标准公务舱", "3UFA": "高端经济舱", "3UFF": "标准头等舱", "3UFI": "空中头等舱", "3UFJ": "公务舱子舱位", "3UX": "特价舱",
    "3UYE": "折扣经济舱", "3UYG": "折扣经济舱", "3UYH": "折扣经济舱", "3UYK": "特价舱", "3UYL": "折扣经济舱", "3UYM": "折扣经济舱",
    "3UYN": "特价舱", "3UYQ": "折扣经济舱", "3UYR": "折扣经济舱", "3UYS": "折扣经济舱", "3UYT": "折扣经济舱", "3UYV": "折扣经济舱",
    "3UYW": "特价舱", "3UYY": "标准经济舱",
    "8LFA": "头等子舱位", "8LFF": "标准头等舱", "8LYB": "折扣经济舱", "8LYD": "特价舱", "8LYE": "折扣经济舱", "8LYH": "折扣经济舱",
    "8LYI": "特价舱", "8LYK": "折扣经济舱", "8LYL": "折扣经济舱", "8LYM": "折扣经济舱", "8LYQ": "折扣经济舱", "8LYT": "特价舱",
    "8LYU": "折扣经济舱", "8LYX": "折扣经济舱", "8LYY": "折扣经济舱", "8LYZ": "特价舱",
    "BKFA": "超值头等舱", "BKFF": "标准头等舱", "BKWW": "超值经济舱", "BKYB": "折扣经济舱", "BKYD": "折扣经济舱", "BKYE": "折扣经济舱",
    "BKYH": "折扣经济舱", "BKYK": "折扣经济舱", "BKYL": "折扣经济舱", "BKYM": "折扣经济舱", "BKYN": "折扣经济舱", "BKYQ": "折扣经济舱",
    "BKYT": "折扣经济舱", "BKYU": "折扣经济舱", "BKYY": "标准经济舱",
    "CAFA": "超值头等舱", "CAFF": "标准头等舱", "CAGG": "超值经济舱", "CAJC": "标准公务舱", "CAJD": "超值公务舱", "CAJJ": "标准公务舱",
    "CAPP": "超值头等舱", "CAYB": "折扣经济舱", "CAYH": "折扣经济舱", "CAYK": "特价舱", "CAYL": "特价舱", "CAYM": "折扣经济舱",
    "CAYQ": "折扣经济舱", "CAYS": "折扣经济舱", "CAYU": "折扣经济舱", "CAYV": "折扣经济舱", "CAYW": "折扣经济舱", "CAYY": "标准经济舱",
    "CZFF": "标准头等舱", "CZJC": "公务舱子舱位", "CZJD": "公务舱子舱位", "CZJI": "公务舱子舱位", "CZJJ": "标准公务舱", "CZWS": "高端经济舱",
    "CZWW": "高端经济舱", "CZYA": "折扣经济舱", "CZYB": "折扣经济舱", "CZYE": "折扣经济舱", "CZYH": "折扣经济舱", "CZYL": "折扣经济舱",
    "CZYM": "折扣经济舱", "CZYR": "特价舱", "CZYT": "特价舱", "CZYU": "折扣经济舱", "CZYV": "折扣经济舱", "CZYY": "标准经济舱",
    "CZYZ": "折扣经济舱",
    "DRFF": "标准头等舱", "DRYB": "折扣经济舱", "DRYE": "折扣经济舱", "DRYH": "折扣经济舱", "DRYK": "折扣经济舱", "DRYN": "折扣经济舱",
    "DRYR": "折扣经济舱", "DRYS": "折扣经济舱", "DRYV": "折扣经济舱", "DRYY": "标准经济舱",
    "DZFA": "头等促销舱", "DZFF": "标准头等舱", "DZYB": "折扣经济舱", "DZYG": "折扣经济舱", "DZYH": "折扣经济舱", "DZYJ": "折扣经济舱",
    "DZYK": "折扣经济舱", "DZYL": "折扣经济舱", "DZYM": "折扣经济舱", "DZYQ": "折扣经济舱", "DZYT": "折扣经济舱", "DZYV": "折扣经济舱",
    "DZYW": "折扣经济舱", "DZYY": "标准经济舱", "DZYZ": "折扣经济舱",
    "EUFF": "标准头等舱", "EUYD": "特价舱", "EUYE": "折扣经济舱", "EUYG": "折扣经济舱", "EUYH": "折扣经济舱", "EUYK": "折扣经济舱",
    "EUYL": "折扣经济舱", "EUYM": "折扣经济舱", "EUYN": "特价舱", "EUYQ": "折扣经济舱", "EUYR": "折扣经济舱", "EUYS": "折扣经济舱",
    "EUYT": "折扣经济舱", "EUYV": "折扣经济舱", "EUYY": "标准经济舱", "EUYZ": "特价舱",
    "FMFF": "标准头等舱", "FMFP": "头等促销舱", "FMJC": "公务舱子舱位", "FMJD": "公务舱折扣舱", "FMJI": "超值公务舱", "FMJJ": "标准公务舱",
    "FMYB": "折扣经济舱", "FMYE": "折扣经济舱", "FMYH": "折扣经济舱", "FMYK": "折扣经济舱", "FMYL": "折扣经济舱", "FMYM": "折扣经济舱",
    "FMYN": "折扣经济舱", "FMYR": "折扣经济舱", "FMYS": "折扣经济舱", "FMYT": "特价舱", "FMYV": "折扣经济舱", "FMYY": "标准经济舱",
    "FMYZ": "预售特价舱",
    "FUFA": "超值头等舱", "FUFF": "标准头等舱", "FUFZ": "超值头等舱", "FUYB": "折扣经济舱", "FUYE": "折扣经济舱", "FUYH": "折扣经济舱",
    "FUYI": "特价舱", "FUYK": "豪华头等舱", "FUYL": "折扣经济舱", "FUYM": "折扣经济舱", "FUYQ": "折扣经济舱", "FUYT": "特价舱",
    "FUYU": "折扣经济舱", "FUYX": "折扣经济舱", "FUYY": "标准经济舱",
    "G5FF": "标准头等舱", "G5YE": "折扣经济舱", "G5YG": "折扣经济舱", "G5YH": "折扣经济舱", "G5YL": "折扣经济舱", "G5YM": "折扣经济舱",
    "G5YO": "折扣经济舱", "G5YQ": "折扣经济舱", "G5YR": "折扣经济舱", "G5YS": "折扣经济舱", "G5YT": "折扣经济舱", "G5YU": "折扣经济舱",
    "G5YV": "折扣经济舱", "G5YY": "标准经济舱",
    "GJRR": "折扣经济舱", "GJYB": "折扣经济舱", "GJYD": "特价舱", "GJYE": "特价舱", "GJYG": "折扣经济舱", "GJYH": "折扣经济舱",
    "GJYI": "特价舱", "GJYK": "折扣经济舱", "GJYL": "折扣经济舱", "GJYM": "折扣经济舱", "GJYP": "折扣经济舱", "GJYQ": "折扣经济舱",
    "GJYS": "超值经济舱", "GJYU": "折扣经济舱", "GJYV": "折扣经济舱", "GJYY": "标准经济舱", "GJYZ": "折扣经济舱",
    "GSYB": "折扣经济舱", "GSYE": "折扣经济舱", "GSYH": "折扣经济舱", "GSYK": "折扣经济舱", "GSYL": "折扣经济舱", "GSYM": "折扣经济舱",
    "GSYQ": "折扣经济舱", "GSYT": "特价舱", "GSYU": "折扣经济舱", "GSYX": "折扣经济舱", "GSYY": "标准经济舱", "GSYZ": "特价舱",
    "HOCC": "标准公务舱", "HOCD": "公务舱子舱位", "HOFA": "超值头等舱", "HOFF": "标准头等舱", "HOYB": "折扣经济舱", "HOYE": "折扣经济舱",
    "HOYH": "折扣经济舱", "HOYK": "折扣经济舱", "HOYL": "折扣经济舱", "HOYM": "折扣经济舱", "HOYP": "特价舱", "HOYQ": "折扣经济舱",
    "HOYR": "折扣经济舱", "HOYT": "折扣经济舱", "HOYV": "折扣经济舱", "HOYW": "折扣经济舱", "HOYX": "预售特价舱", "HOYY": "标准经济舱",
    "HOYZ": "特价舱",
    "HUCC": "标准公务舱", "HUCD": "公务舱子舱位", "HUCI": "公务舱子舱位", "HUFA": "空中头等舱", "HUFF": "标准头等舱", "HUFZ": "空中头等舱",
    "HUYB": "折扣经济舱", "HUYE": "折扣经济舱", "HUYH": "折扣经济舱", "HUYK": "折扣经济舱", "HUYL": "折扣经济舱", "HUYM": "折扣经济舱",
    "HUYN": "折扣经济舱", "HUYQ": "折扣经济舱", "HUYT": "特价舱", "HUYU": "折扣经济舱", "HUYW": "特价舱", "HUYX": "折扣经济舱",
    "HUYY": "标准经济舱",
    "JDCC": "标准公务舱", "JDCD": "公务舱子舱位", "JDCJ": "公务舱子舱位", "JDYB": "折扣经济舱", "JDYE": "折扣经济舱", "JDYH": "折扣经济舱",
    "JDYK": "折扣经济舱", "JDYL": "折扣经济舱", "JDYM": "折扣经济舱", "JDYN": "折扣经济舱", "JDYQ": "折扣经济舱", "JDYS": "特价舱",
    "JDYT": "特价舱", "JDYU": "折扣经济舱", "JDYV": "特价舱", "JDYX": "折扣经济舱", "JDYY": "标准经济舱", "JDYZ": "特价舱",
    "KNWP": "头等促销舱", "KNWW": "超值经济舱", "KNYA": "折扣经济舱", "KNYB": "折扣经济舱", "KNYE": "折扣经济舱", "KNYH": "折扣经济舱",
    "KNYM": "折扣经济舱", "KNYY": "标准经济舱",
    "KYCC": "标准公务舱", "KYFA": "超值经济舱", "KYFF": "标准头等舱", "KYFP": "超值头等舱", "KYYB": "折扣经济舱", "KYYD": "特价舱",
    "KYYE": "折扣经济舱", "KYYH": "折扣经济舱", "KYYJ": "特价舱", "KYYM": "折扣经济舱", "KYYQ": "折扣经济舱", "KYYS": "折扣经济舱",
    "KYYU": "折扣经济舱", "KYYV": "折扣经济舱", "KYYW": "折扣经济舱", "KYYY": "标准经济舱",
    "MFFF": "标准头等舱", "MFJC": "公务舱折扣舱", "MFJD": "公务舱子舱位", "MFJI": "公务舱子舱位", "MFJJ": "标准公务舱", "MFYB": "折扣经济舱",
    "MFYH": "折扣经济舱", "MFYK": "折扣经济舱", "MFYL": "折扣经济舱", "MFYM": "折扣经济舱", "MFYN": "折扣经济舱", "MFYQ": "折扣经济舱",
    "MFYR": "折扣经济舱", "MFYT": "折扣经济舱", "MFYU": "特价舱", "MFYV": "折扣经济舱", "MFYY": "标准经济舱",
    "MUFF": "标准头等舱", "MUFP": "头等促销舱", "MUJC": "公务舱子舱位", "MUJD": "公务舱折扣舱", "MUJI": "超值公务舱", "MUJJ": "标准公务舱",
    "MUUU": "兑换舱", "MUYB": "折扣经济舱", "MUYE": "折扣经济舱", "MUYH": "折扣经济舱", "MUYK": "折扣经济舱", "MUYL": "折扣经济舱",
    "MUYM": "折扣经济舱", "MUYN": "折扣经济舱", "MUYR": "折扣经济舱", "MUYS": "折扣经济舱", "MUYT": "特价舱", "MUYV": "折扣经济舱",
    "MUYY": "标准经济舱", "MUYZ": "预售特价舱",
    "PNCC": "特价舱", "PNYA": "特价舱", "PNYB": "折扣经济舱", "PNYD": "折扣经济舱", "PNYH": "折扣经济舱", "PNYK": "折扣经济舱",
    "PNYL": "折扣经济舱", "PNYM": "折扣经济舱", "PNYQ": "折扣经济舱", "PNYR": "折扣经济舱", "PNYU": "折扣经济舱", "PNYX": "折扣经济舱",
    "PNYY": "折扣经济舱",
    "QWCI": "豪华经济特价舱", "QWCW": "超值经济舱", "QWFA": "折扣经济舱", "QWFF": "标准头等舱", "QWYB": "折扣经济舱", "QWYE": "特价舱",
    "QWYH": "折扣经济舱", "QWYL": "折扣经济舱", "QWYQ": "折扣经济舱", "QWYR": "特价舱", "QWYU": "折扣经济舱", "QWYV": "折扣经济舱",
    "QWYY": "标准经济舱", "QWYZ": "折扣经济舱",
    "SCFA": "头等舱子舱位", "SCFF": "标准头等舱", "SCWR": "高端经济舱", "SCWW": "豪华经济舱", "SCYB": "折扣经济舱", "SCYE": "特价舱",
    "SCYG": "折扣经济舱", "SCYH": "折扣经济舱", "SCYK": "折扣经济舱", "SCYL": "折扣经济舱", "SCYM": "折扣经济舱", "SCYP": "折扣经济舱",
    "SCYQ": "折扣经济舱", "SCYS": "联程舱", "SCYT": "往返舱", "SCYU": "折扣经济舱", "SCYV": "折扣经济舱", "SCYY": "标准经济舱",
    "SCYZ": "折扣经济舱",
    "TVCC": "标准经济舱", "TVFF": "标准头等舱", "TVWW": "超值经济舱", "TVYB": "折扣经济舱", "TVYD": "特价舱", "TVYG": "折扣经济舱",
    "TVYH": "折扣经济舱", "TVYJ": "折扣经济舱", "TVYK": "折扣经济舱", "TVYL": "折扣经济舱", "TVYM": "折扣经济舱", "TVYQ": "折扣经济舱",
    "TVYY": "标准经济舱", "Y8B": "折扣经济舱", "Y8C": "标准公务舱", "Y8D": "公务舱子舱位", "Y8E": "折扣经济舱", "Y8H": "折扣经济舱",
    "Y8I": "公务舱子舱位", "Y8K": "折扣经济舱", "Y8L": "折扣经济舱", "Y8M": "折扣经济舱", "Y8N": "折扣经济舱", "Y8Q": "折扣经济舱",
    "Y8T": "特价舱", "Y8U": "折扣经济舱", "Y8X": "折扣经济舱", "Y8Y": "标准经济舱",
    "ZHCC": "标准公务舱", "ZHCD": "公务舱子舱位", "ZHFA": "豪华头等舱", "ZHFF": "标准头等舱", "ZHFP": "豪华头等舱", "ZHYB": "折扣经济舱",
    "ZHYE": "折扣经济舱", "ZHYH": "折扣经济舱", "ZHYK": "特价舱", "ZHYL": "特价舱", "ZHYM": "折扣经济舱", "ZHYQ": "折扣经济舱",
    "ZHYS": "折扣经济舱", "ZHYU": "折扣经济舱", "ZHYV": "折扣经济舱", "ZHYW": "折扣经济舱", "ZHYY": "标准经济舱"
}

QUNAR_JIPIAO_URL = "http://iteav.baitour.com/CoManage/API/AVService.asmx/GetAVInfo"
QUNAR_JIPIAO_AGENT_CODE = 'B2B_073122'
QUNAR_JIPIAO_AGENT_USER_NAME = 'boluome.com'
QUNAR_JIPIAO_AGENT_PWD = 'boluome.com'
QUNAR_JIPIAO_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

QUNAR_JIPIAO_HOT_LINES = [
    'CAN-TSN', 'SHA-TNA', 'BJS-CGO', 'CAN-FOC', 'BJS-XMN', 'SHA-FOC', 'BJS-KHN', 'SZX-CKG', 'CGO-CAN',
    'KMG-SZX', 'TNA-SHA', 'CGO-SZX', 'CAN-TNA', 'SZX-TNA', 'CGO-BJS', 'NNG-SHA',
    'HGH-CAN', 'KMG-BJS', 'CAN-SYX', 'SIA-CAN', 'KMG-SHA', 'SHA-WUH', 'SHA-CGO', 'SZX-SHA', 'HFE-BJS',
    'XMN-BJS', 'SHA-NNG', 'SYX-CAN', 'BJS-TAO', 'SZX-TAO', 'DLC-SZX', 'SHA-CTU', 'FOC-SHA',
    'CAN-SIA', 'CAN-DLC', 'CAN-NKG', 'SHA-XMN', 'CAN-CGO', 'SIA-BJS', 'DLC-BJS', 'KMG-CTU', 'BJS-KMG',
    'CAN-XMN', 'BJS-WUH', 'TSN-CAN', 'NKG-SHA', 'SHA-TSN', 'SHA-CSX', 'FOC-SZX', 'SZX-CTU',
    'SZX-FOC', 'XMN-CAN', 'CSX-CAN', 'NKG-CAN', 'SHA-SZX', 'CAN-TAO', 'BJS-NKG', 'SIA-SZX', 'CSX-SZX',
    'CSX-BJS', 'BJS-SZX', 'SYX-BJS', 'SZX-CSX', 'BJS-CAN', 'SZX-HGH', 'SHA-SYX', 'CKG-CAN', 'SZX-XMN',
    'SHA-KMG', 'BJS-HET', 'BJS-CKG', 'TAO-BJS', 'HET-BJS', 'TNA-CAN', 'CTU-SZX', 'SHA-DLC', 'CAN-WUH',
    'CAN-BJS', 'SZX-DLC', 'XMN-SZX', 'KMG-CAN', 'WUH-SZX', 'BJS-TNA', 'FOC-CAN', 'SYX-SZX', 'SHE-BJS',
    'SHA-KWE', 'BJS-DLC', 'KWE-SHA', 'SYX-SHA', 'SHA-HRB', 'BJS-CSX', 'XMN-SHA', 'CAN-KMG', 'NKG-SZX',
    'CGO-SHA', 'WUH-CAN', 'CAN-CTU', 'SHA-SIA', 'CKG-SZX', 'TAO-SHA', 'CSX-SHA', 'TAO-SZX', 'SHA-CKG',
    'SIA-SHA', 'HGH-SZX', 'SZX-TSN', 'SZX-NKG', 'DLC-CAN', 'SHA-BJS', 'TNA-SZX', 'NKG-BJS', 'SZX-SIA',
    'HRB-SHA', 'HGH-BJS', 'CAN-HGH', 'DLC-SHA', 'SZX-KMG', 'BJS-CTU', 'FOC-BJS', 'CKG-BJS', 'TAO-CAN',
    'BJS-HGH', 'CTU-BJS', 'CAN-SHA', 'CAN-CSX', 'KHN-BJS', 'BJS-SYX', 'TNA-BJS', 'BJS-SHE', 'CTU-SHA',
    'BJS-SHA', 'SHA-NKG', 'CTU-KMG', 'SZX-CGO', 'CKG-SHA', 'WUH-BJS', 'SZX-SYX', 'TSN-SHA',
    'CTU-CAN', 'BJS-HFE', 'SHA-TAO', 'CAN-CKG', 'SHA-CAN', 'WUH-SHA', 'SZX-BJS', 'SZX-WUH', 'BJS-FOC',
    'TSN-SZX', 'BJS-SIA'
]
QUNAR_JIPIAO_CABIN_MAP = {
    'MFU': '经济舱', 'MFY': '经济舱', 'MFM': '经济舱', 'MFS': '经济舱', 'MFL': '经济舱', 'MFC': '公务舱', 'MFH': '经济舱', 'MFI': '公务舱', 'MFN': '经济舱', 'MFT': '经济舱', 'MFJ': '公务舱', 'MFP': '头等舱', 'MFK': '经济舱', 'MFQ': '经济舱', 'MFA': '头等舱', 'MFD': '公务舱', 'MFF': '头等舱', 'MFR': '经济舱', 'MFB': '经济舱', 'MFV': '经济舱',
    'GYV': '经济舱', 'GYZ': '经济舱', 'GYC': '公务舱', 'GYQ': '经济舱', 'GYH': '经济舱', 'GYK': '经济舱', 'GYM': '经济舱', 'GYL': '经济舱', 'GYB': '经济舱', 'GYP': '经济舱', 'GYI': '经济舱', 'GYF': '头等舱', 'GYR': '经济舱', 'GYG': '经济舱', 'GYE': '经济舱', 'GYJ': '经济舱', 'GYT': '经济舱', 'GYY': '经济舱', 'GYW': '经济舱', 'GYU': '经济舱',
    'KNA': '经济舱', 'KNH': '经济舱', 'KNZ': '经济舱', 'KNI': '经济舱', 'KNP': '公务舱', 'KNE': '经济舱', 'KNF': '头等舱', 'KNM': '经济舱', 'KNN': '经济舱', 'KNW': '公务舱', 'KNB': '经济舱', 'KND': '经济舱', 'KNQ': '经济舱', 'KNT': '经济舱', 'KNJ': '经济舱', 'KNC': '公务舱', 'KNK': '经济舱', 'KNV': '经济舱', 'KNY': '经济舱', 'KNL': '经济舱', 'KNR': '经济舱', 'KNS': '经济舱', 'KNG': '经济舱',
    'G5C': '公务舱', 'G5O': '经济舱', 'G5S': '经济舱', 'G5J': '经济舱', 'G5K': '经济舱', 'G5X': '经济舱', 'G5U': '经济舱', 'G5V': '经济舱', 'G5B': '经济舱', 'G5L': '经济舱', 'G5Z': '经济舱', 'G5A': '头等舱', 'G5G': '经济舱', 'G5P': '经济舱', 'G5Q': '经济舱', 'G5F': '头等舱', 'G5H': '经济舱', 'G5I': '经济舱', 'G5E': '经济舱', 'G5M': '经济舱', 'G5T': '经济舱', 'G5R': '经济舱', 'G5N': '经济舱', 'G5Y': '经济舱',
    '8LK': '经济舱', '8LB': '经济舱', '8LX': '经济舱', '8LV': '经济舱', '8LI': '经济舱', '8LY': '经济舱', '8LT': '经济舱', '8LM': '经济舱', '8LC': '公务舱', '8LU': '经济舱', '8LZ': '经济舱', '8LE': '经济舱', '8LF': '头等舱', '8LH': '经济舱', '8LQ': '经济舱', '8LD': '经济舱', '8LL': '经济舱',
    'JRS': '经济舱', 'JRV': '经济舱', 'JRG': '经济舱', 'JRQ': '经济舱', 'JRW': '经济舱', 'JRB': '经济舱', 'JRH': '经济舱', 'JRR': '经济舱', 'JRO': '经济舱', 'JRP': '经济舱', 'JRT': '经济舱', 'JRM': '经济舱', 'JRN': '经济舱', 'JRX': '经济舱', 'JRY': '经济舱',
    'GTZ': '经济舱', 'GTY': '经济舱', 'GTM': '经济舱', 'GTS': '经济舱', 'GTC': '经济舱', 'GTH': '经济舱', 'GTU': '经济舱', 'GTB': '经济舱', 'GTT': '经济舱', 'GTX': '经济舱', 'GTD': '经济舱', 'GTJ': '经济舱', 'GTK': '经济舱', 'GTE': '经济舱', 'GTQ': '经济舱', 'GTL': '经济舱',
    '3UV': '经济舱', '3UA': '头等舱', '3UH': '经济舱', '3UJ': '公务舱', '3UQ': '经济舱', '3UR': '经济舱', '3UT': '经济舱', '3UK': '经济舱', '3UX': '经济舱', '3UI': '头等舱', '3UM': '经济舱', '3UC': '公务舱', '3US': '经济舱', '3UE': '经济舱', '3UF': '头等舱', '3UN': '经济舱', '3UG': '经济舱', '3UZ': '经济舱', '3UY': '经济舱', '3UL': '经济舱', '3UW': '经济舱',
    'DZE': '经济舱', 'DZM': '经济舱', 'DZV': '经济舱', 'DZJ': '经济舱', 'DZU': '经济舱', 'DZY': '经济舱', 'DZD': '公务舱', 'DZF': '头等舱', 'DZL': '经济舱', 'DZH': '经济舱', 'DZT': '经济舱', 'DZS': '经济舱', 'DZZ': '经济舱', 'DZA': '头等舱', 'DZQ': '经济舱', 'DZC': '经济舱', 'DZW': '经济舱', 'DZK': '经济舱', 'DZB': '经济舱', 'DZP': '经济舱', 'DZG': '经济舱',
    'PNH': '经济舱', 'PNX': '经济舱', 'PND': '经济舱', 'PNW': '经济舱', 'PNQ': '经济舱', 'PNT': '经济舱', 'PNM': '经济舱', 'PNA': '经济舱', 'PNJ': '经济舱', 'PNK': '经济舱', 'PNZ': '经济舱', 'PNE': '经济舱', 'PNB': '经济舱', 'PNC': '公务舱', 'PNL': '经济舱', 'PNV': '经济舱', 'PNI': '经济舱', 'PNN': '经济舱', 'PNY': '经济舱', 'PNU': '经济舱', 'PNR': '经济舱',
    'FMQ': '经济舱', 'FMZ': '经济舱', 'FMH': '经济舱', 'FMT': '经济舱', 'FML': '经济舱', 'FMV': '经济舱', 'FME': '经济舱', 'FMC': '公务舱', 'FMN': '经济舱', 'FMU': '头等舱', 'FMM': '经济舱', 'FMB': '经济舱', 'FMR': '经济舱', 'FMI': '经济舱', 'FMK': '经济舱', 'FMW': '经济舱', 'FMJ': '公务舱', 'FMS': '经济舱', 'FMF': '头等舱', 'FMY': '经济舱', 'FMP': '头等舱', 'FMG': '经济舱',
    'FUM': '经济舱', 'FUI': '经济舱', 'FUY': '经济舱', 'FUX': '经济舱', 'FUL': '经济舱', 'FUQ': '经济舱', 'FUA': '头等舱', 'FUZ': '头等舱', 'FUT': '经济舱', 'FUU': '经济舱', 'FUR': '经济舱', 'FUN': '经济舱', 'FUS': '经济舱', 'FUF': '头等舱', 'FUK': '经济舱', 'FUH': '经济舱', 'FUE': '经济舱', 'FUB': '经济舱',
    'HUK': '经济舱', 'HUN': '经济舱', 'HUY': '经济舱', 'HUA': '头等舱', 'HUH': '经济舱', 'HUQ': '经济舱', 'HUW': '经济舱', 'HUI': '公务舱', 'HUX': '经济舱', 'HUF': '头等舱', 'HUT': '经济舱', 'HUB': '经济舱', 'HUL': '经济舱', 'HUM': '经济舱', 'HUD': '公务舱', 'HUV': '经济舱', 'HUU': '经济舱', 'HUZ': '头等舱', 'HUE': '经济舱', 'HUC': '公务舱',
    'SCB': '经济舱', 'SCZ': '经济舱', 'SCA': '头等舱', 'SCG': '经济舱', 'SCL': '经济舱', 'SCC': '公务舱', 'SCY': '经济舱', 'SCQ': '经济舱', 'SCK': '经济舱', 'SCV': '经济舱', 'SCM': '经济舱', 'SCT': '经济舱', 'SCU': '经济舱', 'SCS': '经济舱', 'SCD': '公务舱', 'SCH': '经济舱', 'SCP': '经济舱', 'SCR': '经济舱', 'SCF': '头等舱', 'SCW': '经济舱', 'SCE': '经济舱',
    'MUM': '经济舱', 'MUY': '经济舱', 'MUJ': '公务舱', 'MUZ': '经济舱', 'MUV': '经济舱', 'MUK': '经济舱', 'MUS': '经济舱', 'MUE': '经济舱', 'MUR': '经济舱', 'MUD': '公务舱', 'MUB': '经济舱', 'MUQ': '经济舱', 'MUI': '经济舱', 'MUH': '经济舱', 'MUC': '公务舱', 'MUG': '经济舱', 'MUW': '经济舱', 'MUU': '头等舱', 'MUF': '头等舱', 'MUL': '经济舱', 'MUT': '经济舱', 'MUP': '头等舱', 'MUN': '经济舱',
    'QWC': '公务舱', 'QWQ': '经济舱', 'QWP': '经济舱', 'QWW': '经济舱', 'QWF': '头等舱', 'QWT': '经济舱', 'QWB': '经济舱', 'QWH': '经济舱', 'QWA': '头等舱', 'QWY': '经济舱', 'QWL': '经济舱', 'QWU': '经济舱', 'QWK': '经济舱', 'QWE': '经济舱', 'QWR': '经济舱', 'QWI': '经济舱', 'QWZ': '经济舱', 'QWM': '经济舱', 'QWG': '经济舱', 'QWV': '经济舱',
    'HOD': '公务舱', 'HOA': '头等舱', 'HOQ': '经济舱', 'HOH': '经济舱', 'HOK': '经济舱', 'HOV': '经济舱', 'HOP': '经济舱', 'HOS': '经济舱', 'HOC': '公务舱', 'HOF': '头等舱', 'HOY': '经济舱', 'HOM': '经济舱', 'HOR': '经济舱', 'HOT': '经济舱', 'HOL': '经济舱', 'HOI': '经济舱', 'HOW': '经济舱', 'HOU': '经济舱', 'HOX': '经济舱', 'HOE': '经济舱', 'HOZ': '经济舱', 'HOB': '经济舱',
    'CAH': '经济舱', 'CAF': '头等舱', 'CAS': '经济舱', 'CAC': '公务舱', 'CAP': '头等舱', 'CAD': '公务舱', 'CAV': '经济舱', 'CAG': '经济舱', 'CAB': '经济舱', 'CAT': '经济舱', 'CAY': '经济舱', 'CAU': '经济舱', 'CAQ': '经济舱', 'CAJ': '公务舱', 'CAM': '经济舱', 'CAA': '头等舱', 'CAK': '经济舱', 'CAL': '经济舱', 'CAW': '经济舱',
    'EUS': '经济舱', 'EUT': '经济舱', 'EUH': '经济舱', 'EUR': '经济舱', 'EUE': '经济舱', 'EUZ': '经济舱', 'EUM': '经济舱', 'EUV': '经济舱', 'EUK': '经济舱', 'EUW': '经济舱', 'EUN': '经济舱', 'EUI': '经济舱', 'EUL': '经济舱', 'EUF': '头等舱', 'EUC': '公务舱', 'EUJ': '公务舱', 'EUQ': '经济舱', 'EUA': '头等舱', 'EUG': '经济舱', 'EUY': '经济舱', 'EUD': '经济舱',
    'KYH': '经济舱', 'KYI': '经济舱', 'KYG': '经济舱', 'KYU': '经济舱', 'KYW': '经济舱', 'KYY': '经济舱', 'KYQ': '经济舱', 'KYC': '公务舱', 'KYF': '头等舱', 'KYP': '头等舱', 'KYA': '头等舱', 'KYL': '经济舱', 'KYS': '经济舱', 'KYT': '经济舱', 'KYE': '经济舱', 'KYV': '经济舱', 'KYM': '经济舱', 'KYR': '经济舱', 'KYJ': '经济舱', 'KYD': '经济舱', 'KYZ': '经济舱', 'KYB': '经济舱',
    'GSC': '公务舱', 'GSM': '经济舱', 'GSX': '经济舱', 'GSQ': '经济舱', 'GSY': '经济舱', 'GSK': '经济舱', 'GSI': '头等舱', 'GSU': '经济舱', 'GSL': '经济舱', 'GSE': '经济舱', 'GSP': '头等舱', 'GSB': '经济舱', 'GSF': '头等舱', 'GST': '经济舱', 'GSZ': '经济舱', 'GSA': '头等舱', 'GSH': '经济舱',
    'RYJ': '公务舱', 'RYY': '经济舱', 'RYI': '经济舱', 'RYN': '经济舱', 'RYZ': '经济舱', 'RYC': '公务舱', 'RYR': '经济舱', 'RYM': '经济舱', 'RYD': '公务舱', 'RYQ': '经济舱', 'RYB': '经济舱', 'RYT': '经济舱', 'RYV': '经济舱', 'RYL': '经济舱', 'RYU': '经济舱', 'RYF': '头等舱', 'RYK': '经济舱', 'RYH': '经济舱',
    'Y8M': '经济舱', 'Y8B': '经济舱', 'Y8H': '经济舱', 'Y8V': '经济舱', 'Y8L': '经济舱', 'Y8X': '经济舱', 'Y8E': '经济舱', 'Y8T': '经济舱', 'Y8G': '经济舱', 'Y8Q': '经济舱', 'Y8Y': '经济舱', 'Y8U': '经济舱', 'Y8D': '公务舱', 'Y8C': '公务舱', 'Y8K': '经济舱', 'Y8N': '经济舱',
    'A6T': '经济舱', 'A6U': '经济舱', 'A6F': '头等舱', 'A6M': '经济舱', 'A6G': '经济舱', 'A6H': '经济舱', 'A6A': '经济舱', 'A6R': '经济舱', 'A6I': '经济舱', 'A6B': '经济舱', 'A6J': '经济舱', 'A6X': '经济舱', 'A6Y': '经济舱', 'A6Q': '经济舱', 'A6C': '公务舱', 'A6V': '经济舱', 'A6O': '经济舱', 'A6K': '经济舱', 'A6L': '经济舱', 'A6N': '经济舱',
    'NSB': '经济舱', 'NSM': '经济舱', 'NSZ': '经济舱', 'NSN': '经济舱', 'NSV': '经济舱', 'NSK': '经济舱', 'NSS': '经济舱', 'NSH': '经济舱', 'NSC': '公务舱', 'NSA': '头等舱', 'NSI': '公务舱', 'NSL': '经济舱', 'NSY': '经济舱', 'NSJ': '公务舱', 'NSQ': '经济舱', 'NST': '经济舱', 'NSW': '经济舱', 'NSR': '经济舱',
    'UQT': '经济舱', 'UQQ': '经济舱', 'UQA': '经济舱', 'UQX': '经济舱', 'UQE': '经济舱', 'UQW': '经济舱', 'UQI': '经济舱', 'UQK': '经济舱', 'UQB': '经济舱', 'UQR': '经济舱', 'UQU': '经济舱', 'UQY': '经济舱', 'UQJ': '经济舱', 'UQM': '经济舱', 'UQL': '经济舱', 'UQZ': '经济舱', 'UQD': '经济舱', 'UQH': '经济舱', 'UQC': '公务舱',
    'DRW': '经济舱', 'DRL': '经济舱', 'DRQ': '经济舱', 'DRR': '经济舱', 'DRN': '经济舱', 'DRX': '经济舱', 'DRF': '头等舱', 'DRT': '经济舱', 'DRY': '经济舱', 'DRE': '经济舱', 'DRH': '经济舱', 'DRV': '经济舱', 'DRK': '经济舱', 'DRB': '经济舱', 'DRS': '经济舱', 'DRZ': '经济舱', 'DRI': '经济舱', 'DRP': '头等舱',
    'BKY': '经济舱', 'BKT': '经济舱', 'BKO': '经济舱', 'BKJ': '经济舱', 'BKM': '经济舱', 'BKL': '经济舱', 'BKE': '经济舱', 'BKF': '头等舱', 'BKQ': '经济舱', 'BKD': '经济舱', 'BKC': '公务舱', 'BKZ': '经济舱', 'BKN': '经济舱', 'BKH': '经济舱', 'BKK': '经济舱', 'BKI': '经济舱', 'BKB': '经济舱', 'BKU': '经济舱', 'BKX': '经济舱', 'BKR': '经济舱', 'BKA': '头等舱', 'BKW': '经济舱', 'BKS': '经济舱',
    'TVC': '公务舱', 'TVJ': '经济舱', 'TVG': '经济舱', 'TVL': '经济舱', 'TVF': '头等舱', 'TVT': '经济舱', 'TVI': '经济舱', 'TVQ': '经济舱', 'TVV': '经济舱', 'TVY': '经济舱', 'TVK': '经济舱', 'TVR': '经济舱', 'TVM': '经济舱', 'TVH': '经济舱', 'TVD': '经济舱', 'TVB': '经济舱', 'TVA': '头等舱', 'TVZ': '经济舱', 'TVW': '经济舱', 'TVE': '经济舱',
    'JDD': '公务舱', 'JDZ': '公务舱', 'JDH': '经济舱', 'JDC': '公务舱', 'JDM': '经济舱', 'JDY': '经济舱', 'JDE': '经济舱', 'JDK': '经济舱', 'JDQ': '经济舱', 'JDP': '公务舱', 'JDT': '经济舱', 'JDL': '经济舱', 'JDB': '经济舱', 'JDX': '经济舱', 'JDN': '经济舱', 'JDU': '经济舱', 'JDV': '经济舱',
    'CNX': '经济舱', 'CNZ': '头等舱', 'CNB': '经济舱', 'CNF': '头等舱', 'CNU': '经济舱', 'CND': '公务舱', 'CNL': '经济舱', 'CNI': '公务舱', 'CNC': '公务舱', 'CNK': '经济舱', 'CNT': '经济舱', 'CNA': '头等舱', 'CNM': '经济舱', 'CNQ': '经济舱', 'CNN': '经济舱', 'CNY': '经济舱', 'CNH': '经济舱', 'CNE': '经济舱',
    'GJF': '头等舱', 'GJY': '经济舱', 'GJZ': '经济舱', 'GJR': '经济舱', 'GJM': '经济舱', 'GJA': '头等舱', 'GJC': '公务舱', 'GJG': '经济舱', 'GJX': '经济舱', 'GJU': '经济舱', 'GJI': '经济舱', 'GJQ': '经济舱', 'GJH': '经济舱', 'GJS': '经济舱', 'GJB': '经济舱', 'GJV': '经济舱', 'GJD': '经济舱', 'GJE': '经济舱', 'GJK': '经济舱', 'GJL': '经济舱', 'GJP': '经济舱',
    'GXK': '经济舱', 'GXM': '经济舱', 'GXX': '经济舱', 'GXE': '经济舱', 'GXH': '经济舱', 'GXB': '经济舱', 'GXT': '经济舱', 'GXI': '头等舱', 'GXY': '经济舱', 'GXF': '头等舱', 'GXL': '经济舱', 'GXZ': '经济舱', 'GXQ': '经济舱', 'GXU': '经济舱',
    'ZHQ': '经济舱', 'ZHF': '头等舱', 'ZHG': '经济舱', 'ZHJ': '经济舱', 'ZHA': '头等舱', 'ZHY': '经济舱', 'ZHK': '经济舱', 'ZHE': '经济舱', 'ZHD': '公务舱', 'ZHV': '经济舱', 'ZHB': '经济舱', 'ZHP': '头等舱', 'ZHH': '经济舱', 'ZHL': '经济舱', 'ZHC': '公务舱', 'ZHU': '经济舱', 'ZHS': '经济舱', 'ZHM': '经济舱', 'ZHW': '经济舱', 'ZHT': '经济舱',
    'CZB': '经济舱', 'CZP': '头等舱', 'CZV': '经济舱', 'CZM': '经济舱', 'CZT': '经济舱', 'CZL': '经济舱', 'CZZ': '经济舱', 'CZX': '经济舱', 'CZS': '经济舱', 'CZH': '经济舱', 'CZW': '经济舱', 'CZU': '经济舱', 'CZC': '公务舱', 'CZA': '经济舱', 'CZJ': '公务舱', 'CZI': '头等舱', 'CZY': '经济舱', 'CZD': '公务舱', 'CZE': '经济舱', 'CZR': '经济舱', 'CZF': '头等舱',
    '9HH': '经济舱', '9HT': '经济舱', '9HJ': '经济舱', '9HA': '经济舱', '9HD': '经济舱', '9HY': '经济舱', '9HC': '公务舱', '9HW': '经济舱', '9HL': '经济舱', '9HX': '经济舱', '9HI': '经济舱', '9HE': '经济舱', '9HK': '经济舱', '9HM': '经济舱', '9HZ': '经济舱', '9HP': '经济舱', '9HR': '经济舱', '9HU': '经济舱', '9HB': '经济舱', '9HQ': '经济舱'
}


SCRATCH_KEY = 'scratch:57e3507cea8a682600b1432e'
SCRATCH_ORDER_KEY = 'scratch_order'

INVITE_COUPON_URL = 'http://192.168.2.2:32800/api/v1/marketing/invite_coupon'

COUPON_URL = 'http://stg.web.boluomeet.com/coupon'
