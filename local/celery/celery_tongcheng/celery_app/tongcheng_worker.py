
# coding: utf-8
from __future__ import absolute_import, unicode_literals

import hashlib
import json
import logging
import math
import time

import requests
from celery import Celery, Task, platforms
from pymongo import MongoClient

import conf

platforms.C_FORCE_ROOT = True

tongcheng = Celery(
    'tongcheng_worker',
    broker=conf.MQ_BROKER
)

tongcheng.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERYD_MAX_TASKS_PER_CHILD=200,
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_CREATE_MISSING_QUEUES=True
)


class TongchengTask(Task):
    abstract = True

    def __init__(self):
        self._pmdb = None
        self._smdb = None

    @property
    def pmdb(self):
        if self._pmdb is None:
            _pmc = MongoClient(conf.PRO_MONGO_HOST,
                               replicaset=conf.REPLICASET_NAME)
            self._pmdb = _pmc['boluome']
        return self._pmdb

    @property
    def smdb(self):
        if self._smdb is None:
            _smc = MongoClient(conf.STG_MONGO_HOST,
                               replicaset=conf.REPLICASET_NAME)
            self._smdb = _smc['boluome']
        return self._smdb


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def ticket_incr_fetch(self, inc):
    uri = 'GetTicketIncrementService.ashx'
    sign = hashlib.md5(
        '{}{}{}{}'.format(conf.TONGCHENG_AGENT_ACCOUNT,
                          inc, 20, conf.TONGCHENG_APP_KEY).encode('utf-8')
    ).hexdigest()
    data = {
        "requestHead": {
            "digitalSign": sign,
            "agentAccount": conf.TONGCHENG_AGENT_ACCOUNT
        },
        "requestBody": {
            "maxIncrementId": inc,
            "queryNumber": 20
        }
    }

    try:
        resp = requests.post(
            conf.TONGCHENG_API_SERVER + uri,
            data=json.dumps(data))
        resp_data = resp.json()
    except Exception as e:
        return[inc, e]

    ticket_list = resp_data.get('ticketPriceList', [])
    max_inc_id = resp_data.get('maxIncrementId', inc)

    if max_inc_id == inc:
        self.smdb['inc_id'].update_one(
            {'channel': 'tongcheng'},
            {'$set': {'inc_id': max_inc_id}},
            upsert=True
        )
        return ['increment fetch finished']

    ticket_incr_fetch.apply_async(args=[max_inc_id],
                                  queue=conf.MQ_TONGCHENG)

    new_scenery_id_list = set()
    for ticket in ticket_list:
        if 'ticketPriceId' not in ticket:
            continue

        for del_key in ['BCTTicketPriceMode', 'isCopSys', 'isPreference']:
            ticket.pop(del_key, '')

        ret = self.smdb['menpiao_goods_tongcheng'].update_one(
            {'ticketPriceId': ticket['ticketPriceId']},
            {'$set': ticket},
            upsert=True
        )

        if ret.matched_count == 0:
            new_scenery_id_list.add(ticket['sceneryId'])
            prices_fetch.apply_async(args=[ticket['ticketPriceId']],
                                     queue=conf.MQ_TONGCHENG)

    for scenery_id in new_scenery_id_list:
        scenery_fetch_one.apply_async(args=[scenery_id],
                                      queue=conf.MQ_TONGCHENG)

    return ['increment fetch', inc, max_inc_id]


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def increament_schedule(self):
    try:
        data = self.smdb['inc_id'].find_one({'channel': 'tongcheng'})

        ticket_incr_fetch.apply_async(args=[data['inc_id']],
                                      queue=conf.MQ_TONGCHENG)
    except Exception as e:
        logging.exception(e)


# 更新票价绑定更新所属景区信息
@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def scenery_fetch_one(self, scenery_id):
    uri = 'GetSceneryDetailService.ashx'
    sign = hashlib.md5(
        '{}{}{}'.format(conf.TONGCHENG_AGENT_ACCOUNT,
                        scenery_id, conf.TONGCHENG_APP_KEY).encode('utf-8')
    ).hexdigest()
    data = {
        "requestHead": {
            "digitalSign": sign,
            "agentAccount": conf.TONGCHENG_AGENT_ACCOUNT
        },
        "requestBody": {
            "sceneryId": scenery_id
        }}

    try:
        resp = requests.post(conf.TONGCHENG_API_SERVER + uri,
                             data=json.dumps(data))
        item = resp.json()
    except Exception as e:
        logging.exception(e)

    if 'SceneryID' not in item:
        self.smdb['menpiao_goods_tongcheng'].delete_many(
            {'sceneryId': scenery_id},
        )

    item_dict = {
        'id': item['SceneryID'],
        'name': item.get('SceneryName', None),
        "grade": item.get('SceneryGrade', None),
        'address': item.get('SceneryAddress', None),
        'province': item.get('SceneryProvinceName', None),
        'city': item.get('SceneryCityName', None),
        'summary': item.get('ScenerySummary', None),
        'lng': item.get('SceneryLongitude', None),
        'lat': item.get('SceneryLatitude', None),
        'alias': item.get('SceneryAliasName', None),
        'traffic': item.get('SceneryTrafficGuide', None),
        'notes': item.get('UserNotes', None),
        "introduce": item.get('SceneryDetailIntroduce', None),
        "ticketType": item.get('TicketType', None),
        "ticketTypeName": item.get('TicketTypeName', None),
        "picture": item.get('PictureListInfo', None)
    }

    item_dict = {k: v for k, v in item_dict.items() if v}

    self.smdb['menpiao_scenic_tongcheng'].update_one(
        {'id': item_dict['id']},
        {'$set': item_dict},
        upsert=True
    )

    return ['fetch one scenic', item_dict['id']]


# 各景区-票型价格3个月日历查询接口
@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def prices_fetch(self, ticket_price_id):
    uri = 'GetPriceCalendarInfoService.ashx'
    sign = hashlib.md5(
        '{}{}{}'.format(conf.TONGCHENG_AGENT_ACCOUNT,
                        ticket_price_id, conf.TONGCHENG_APP_KEY).encode('utf-8')
    ).hexdigest()
    # now time
    ts = time.time()
    dt = time.localtime(ts)
    arriva_date = time.strftime('%Y-%m-%d', dt)
    data = {
        "requestHead": {
            "digitalSign": sign,
            "agentAccount": conf.TONGCHENG_AGENT_ACCOUNT
        },
        "requestBody": {
            "PriceId": ticket_price_id,
            "TravelDate": arriva_date,
            "MonthNumber": 3   # 查询现在时刻起3个月
        }
    }
    # post price_id景点的第i页
    resp = requests.post(
        conf.TONGCHENG_API_SERVER + uri,
        data=json.dumps(data)
    )
    resp_data = resp.json()
    price_list = resp_data.get('priceList', [])
    # 遍历i页条目，并插入mongoDB
    if price_list:
        self.smdb['menpiao_goods_tongcheng'].update_one(
            {'ticketPriceId': ticket_price_id},
            {'$set': {'prices': price_list}}
        )
    return ['prices_fetch', ticket_price_id]


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def prices_schedule(self):
    data = self.smdb['menpiao_goods_tongcheng'].find(
        projection={'ticketPriceId': 1, '_id': 0}
    )
    for item in data:
        ticket_fetch.apply_async(args=[item['ticketPriceId']],
                                 queue=conf.MQ_TONGCHENG)


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def scenery_fetch(self, page_index):
    """各地区所有景区查询
    """
    uri = 'GetSceneryListService.ashx'
    # 调用post函数，创建r对象
    sign = hashlib.md5(
        '{}{}{}{}'.format(conf.TONGCHENG_AGENT_ACCOUNT, 20,
                          page_index, conf.TONGCHENG_APP_KEY).encode('utf-8')
    ).hexdigest()
    # data
    data = {
        "requestHead": {
            "digitalSign": sign,
            "agentAccount": conf.TONGCHENG_AGENT_ACCOUNT
        },
        "requestBody": {
            "pageSize": 20,
            "pageIndex": page_index
        }
    }
    # post 第 i 页
    try:
        resp = requests.post(
            conf.TONGCHENG_API_SERVER + uri,
            data=json.dumps(data))
        resp_data = resp.json()
        total_count = resp_data.get('TotalCount', 0)
        scenery_list = resp_data.get('SceneryList', [])
    except Exception as e:
        logging.exception(e)
        return [page_index, resp.text]

    if page_index == 1:
        for i in range(1, math.ceil(float(total_count) / 20)):
            scenery_fetch.apply_async(args=[i + 1],
                                      queue=conf.MQ_TONGCHENG)

    for item in scenery_list:
        if 'SceneryID' not in item:
            continue

        item = {
            'id': item['SceneryID'],
            'name': item.get('SceneryName', None),
            "grade": item.get('SceneryGrade', None),
            'address': item.get('SceneryAddress', None),
            'province': item.get('SceneryProvinceName', None),
            'city': item.get('SceneryCityName', None),
            'summary': item.get('ScenerySummary', None),
            'lng': item.get('SceneryLongitude', None),
            'lat': item.get('SceneryLatitude', None),
            'alias': item.get('SceneryAliasName', None),
            'traffic': item.get('SceneryTrafficGuide', None),
            'notes': item.get('UserNotes', None),
            "introduce": item.get('SceneryDetailIntroduce', None),
            "ticketType": item.get('TicketType', None),
            "ticketTypeName": item.get('TicketTypeName', None),
            "picture": item.get('PictureListInfo', None)
        }
        if item['lat'] and item['lng']:
            item['loc'] = [float(item.get('SceneryLongitude')),
                           float(item.get('SceneryLatitude'))]

        item = {k: v for k, v in item.items() if v}

        self.smdb['menpiao_scenic_tongcheng'].update_one(
            {'id': item['id']},
            {'$set': item},
            upsert=True
        )

    return ['scenery_fetch', page_index]


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def ticket_fetch(self, sce_id, page_index=1):
    """#分销商票型查询接口
    """
    uri = 'GetTicketDetailService.ashx'
    sign = hashlib.md5(
        '{}{}{}{}'.format(conf.TONGCHENG_AGENT_ACCOUNT, 20,
                          page_index, conf.TONGCHENG_APP_KEY).encode('utf-8')
    ).hexdigest()
    data = {
        "requestHead": {
            "digitalSign": sign,
            "agentAccount": conf.TONGCHENG_AGENT_ACCOUNT
        },
        "requestBody": {
            "pageSize": 20,
            "pageIndex": page_index,
            "sceneryId": sce_id  # 景点id
        }}

    try:
        # post sce_id景点的第i页
        resp = requests.post(conf.TONGCHENG_API_SERVER +
                             uri, data=json.dumps(data))
        resp_data = resp.json()
        data = resp_data.get('ticketPriceList', [])
        total_count = resp_data.get('TotalCount', 0)
        if total_count > page_index * 20:
            ticket_fetch.apply_async(args=[sce_id, page_index + 1],
                                     queue=conf.MQ_TONGCHENG)
    except Exception as e:
        logging.exception(e)

    for item in data:
        if 'ticketPriceId' not in item:
            continue

        for del_key in ['BCTTicketPriceMode', 'isCopSys', 'isPreference']:
            item.pop(del_key, '')

        self.smdb['menpiao_goods_tongcheng'].update_one(
            {'ticketPriceId': item['ticketPriceId']},
            {'$set': item},
            upsert=True
        )

        prices_fetch.apply_async(args=[item['ticketPriceId']],
                                 queue=conf.MQ_TONGCHENG)

    return sce_id


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def ticket_start(self):
    sce = self.smdb['menpiao_scenic_tongcheng'].find(
        projection={'id': 1, '_id': 0}
    )  # 获取景点id
    for item in sce:
        ticket_fetch.apply_async(args=[item['id']],
                                 queue=conf.MQ_TONGCHENG)


def binary_search(array, t):
    """二分法删除时间t之前的票价列表，返回t时间对应array的索引
    """
    low = 0
    height = len(array) - 1
    while low <= height:
        mid = math.floor((low + height) / 2)

        if len(array[mid]['date']) != 10:
            try:
                array[mid]['date'] = time.strptime(
                    array[mid]['date'],
                    '%Y-%m-%d'
                )
                t = time.strptime(t, '%Y-%m-%d')
            except Exception as e:
                continue

        if array[mid]['date'] < t:
            low = mid + 1
        elif array[mid]['date'] > t:
            height = mid - 1
        else:
            return mid

    return low


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def remove_old_prices(self, scenery_id, today_date):
    data_prices = self.smdb['menpiao_goods_tongcheng'].find(
        {'sceneryId': scenery_id},
        projection={'prices': 1,
                    'ticketPriceId': 1,
                    'marketPrice': 1,
                    'tcAmountPrice': 1,
                    '_id': 0}
    )

    price = -1
    market_price = -1
    for data_price in data_prices:
        if not data_price.get('prices'):
            continue

        price_index = binary_search(data_price['prices'], today_date)
        if price_index < len(data_price['prices']):
            if price == -1:
                price = data_price.get('tcAmountPrice', -1)
                market_price = data_price.get('marketPrice', -1)
            elif 0 < data_price.get('tcAmountPrice', -1) < price:
                price = data_price['tcAmountPrice']
                market_price = data_price['marketPrice']

            if price_index > 0:
                tmp = (data_price['prices'][0]['date'],
                       data_price['prices'][price_index - 1]['date'])
                data_price['prices'] = data_price['prices'][price_index:]
                if data_price['prices']:
                    self.smdb['menpiao_goods_tongcheng'].update_one(
                        {'ticketPriceId': data_price['ticketPriceId']},
                        {'$set': data_price}
                    )
        else:
            self.smdb['menpiao_goods_tongcheng'].update_one(
                {'ticketPriceId': data_price['ticketPriceId']},
                {'$unset': {'prices': ''}}
            )

    self.smdb['menpiao_scenic_tongcheng'].update_one(
        {'id': scenery_id},
        {'$set': {'price': price, 'marketPrice': market_price}}
    )

    return ['remove_old_prices', scenery_id, price, market_price]


@tongcheng.task(base=TongchengTask, bind=True, ignore_result=True, max_retries=3)
def remove_old_prices_schedule(self):
    """启动"""
    scenery_list = self.smdb['menpiao_scenic_tongcheng'].find(
        projection={'id': 1, '_id': 0}
    )

    today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for scenery in scenery_list:
        remove_old_prices.apply_async(
            args=[scenery['id'], today_date], queue=conf.MQ_TONGCHENG
        )

    return
