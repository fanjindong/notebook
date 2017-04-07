from __future__ import absolute_import, unicode_literals

import hashlib
import json
import time
import traceback

import requests
from celery import Celery, Task, platforms
from pymongo import MongoClient, ReturnDocument

import conf

platforms.C_FORCE_ROOT = True
# 用于开启root也可以启动celery服务，默认是不允许root启动celery的
lvmama = Celery('spider_worker', broker=conf.MQ_BROKER)

lvmama.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERYD_MAX_TASKS_PER_CHILD=200,
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_CREATE_MISSING_QUEUES=True,
)


class LvmamaTask(Task):
    #: If :const:`True` the task is an abstract base class.
    abstract = True
    _pro = None
    _stg = None
    _dev = None

    @property
    def pro(self):
        if self._pro is None:
            _pro = MongoClient(conf.PRO_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._pro = _pro["boluome"]
        return self._pro

    @property
    def stg(self):
        if self._stg is None:
            _stg = MongoClient(conf.STG_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._stg = _stg["boluome"]
        return self._stg

    @property
    def dev(self):
        if self._dev is None:
            _dev = MongoClient(conf.DEV_MONGO_HOST, replicaset=conf.REPLICASET_NAME)
            self._dev = _dev["boluome"]
        return self._dev


api_url = "http://api.lvmama.com/distributorApi/2.0/api/ticketProd/"
app_key = "BOLUOMI"
secret = "5ef1f365cae39119bd04b8afb35b134f"


@Lvmama.task(base=LvmamaTask, bind=True, ignore_result=True, max_retries=3)
def product_ids_fetch():
    for product in self.pro['menpiao_products'].find({}, ['id']):
        product_id = product['id']
        products_info.apply_async(args=[product_id], queue=conf.)
    return


@Lvmama.task(base=LvmamaTask, bind=True, ignore_result=True, max_retries=3)
def products_info(product_ids):
    ts = int(time.time())
    sign = hashlib.md5('{}{}{}'.format(secret, ts, secret).encode('utf-8')).hexdigest()
    key_data = {
        'appKey': app_key,
        'messageFormat': 'json',
        'timestamp': ts,
        'sign': sign,
        'productIds': product_ids
    }
    url = api_url + "/productInfoList"
    resp_data = requests.get(url, params=key_data).json()['productList'][0]
    pprint(resp_data)

    def dict_none():
        return None
    data = defaultdict(dict_none, resp_data)

    def clean_data(data):
        if isinstance(data, str)and ('<![CDATA' in data):
            return data[9:-3]
        return data
    scenic_info = {}
    scenic_info['id'] = clean_data(data['productId'])
    scenic_info['placeId'] = clean_data(data['placeId'])
    scenic_info['placeName'] = clean_data(data['placeName'])
    scenic_info['type'] = clean_data(data['productType'])
    scenic_info['status'] = clean_data(data['productStatus'])
    scenic_info['posts'] = clean_data(data['postList'])
    scenic_info['recommends'] = clean_data(data['recommendList'])
    scenic_info['bookingInfo'] = clean_data(data['bookingInfo'])
    scenic_info['intro'] = clean_data(data['introdution'])
    scenic_info['activities'] = clean_data(data['activities'])
    scenic_info['character'] = clean_data(data['characteristic'])
    scenic_info['playAttractions'] = clean_data(data['playAttractions'])
    scenic_info['productTheme'] = clean_data(data['productTheme'])
    scenic_info['serviceGuarantee'] = clean_data(data['serviceGuarantee'])
    scenic_info['images'] = clean_data(data['images'])
    goods_ids = data['goodsIds']
    print(goods_ids)
    return pprint(scenic_info), goods_ids
products_info(172157)


def good_info_fetch(goods_id):
    ts = int(time.time())
    sign = hashlib.md5('{}{}{}'.format(secret, ts, secret).encode('utf-8')).hexdigest()
    key_data = {
        'appKey': app_key,
        'messageFormat': 'json',
        'timestamp': ts,
        'sign': sign,
        'goodsIds': goods_id
    }
    url = api_url + "/goodInfoList"
    resp_data = requests.get(url, params=key_data).json()['goodsList']
    for item in resp_data:
        def dict_none():
            return None
        data = defaultdict(dict_none, item)

        def clean_data(data):
            if isinstance(data, str)and ('<![CDATA' in data):
                return data[9:-3]
            return data
        good_info = {}
        good_info['id'] = clean_data(data['goodsId'])
        good_info['productId'] = clean_data(data['productId'])
        good_info['standardName'] = clean_data(data['standardName'])
        good_info['name'] = clean_data(data['goodsName'])
        good_info['sort'] = clean_data(data['goodsSort'])
        good_info['paymentType'] = clean_data(data['paymentType'])
        good_info['ticketType'] = clean_data(data['ticketType'])
        good_info['adultTicket'] = clean_data(data['adultTicket'])
        good_info['childTicket'] = clean_data(data['childTicket'])
        good_info['type'] = clean_data(data['goodsType'])
        good_info['certificate'] = clean_data(data['certificate'])
        good_info['status'] = clean_data(data['status'])
        good_info['rules'] = clean_data(data['rules'])
        good_info['effective'] = clean_data(data['effective'])
        good_info['minimum'] = clean_data(data['minimum'])
        good_info['maximum'] = clean_data(data['maximum'])
        good_info['costInclude'] = clean_data(data['costInclude'])
        good_info['notice'] = clean_data(data['notice'])
        good_info['importentPoint'] = clean_data(data['importentPoint'])
        good_info['booker'] = clean_data(data['booker'])
        good_info['traveller'] = clean_data(data['traveller'])

    return pprint(good_info)
good_info_fetch('1740200,1740203,1740226,3800157')
