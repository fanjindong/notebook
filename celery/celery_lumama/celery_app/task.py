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

api_url = "http://api.lvmama.com/distributorApi/2.0/api"
app_key = "BOLUOMI"
secret = "5ef1f365cae39119bd04b8afb35b134f"


class lvmamaTask(Task):
    abstract = True
    _loc = None
    _pro = None

    @property
    def loc(self):
        if self._loc is None:
            _loc = MongoClient('mongodb://localhost:27017')
            self._loc = _loc["test"]
        return self._loc

    @property
    def pro(self):
        if self._pro is None:
            _pro = MongoClient(
                'mongodb://mongoc:Boluome123@139.198.1.168:10017/')
            self._pro = _pro["boluome"]
        return self._pro


@app.task(base=lvmamaTask, bind=True, ignore_result=True, max_retries=3)
def scenic_info(self, scenic_id):
    ts = int(time.time())
    sign = hashlib.md5('{}{}{}'.format(
        secret, ts, secret).encode('utf-8')).hexdigest()
    key_data = {
        'appKey': app_key,
        'messageFormat': 'json',
        'timestamp': ts,
        'sign': sign,
        'scenicId': scenic_id
    }
    url = api_url + "/ticketProd/scenicInfoList"
    try:
        data = requests.get(url, params=key_data).json()['scenicNameList'][0]
    except KeyError as e:
        scenic_info.delay(scenic_id)
        return [scenic_id, 'again']

    def clean_data(data):
        if isinstance(data, str)and ('<![CDATA' in data):
            return data[9:-3]
        return data

    def judgment(keys, data=data, default=[]):
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

    scenic_info = {}
    scenic_info['id'] = clean_data(data['scenicId'])
    scenic_info['info'] = clean_data(judgment('placeInfo'))
    scenic_info['city'] = clean_data(judgment('placeCity'))
    scenic_info['province'] = clean_data(judgment(['placeProvince']))
    scenic_info['addr'] = clean_data(judgment('placeToAddr'))
    scenic_info['level'] = clean_data(judgment('placeLevel'))
    scenic_info['loc'] = [clean_data(judgment(['googleData', 'longitude'])),
                          clean_data(judgment(['googleData', 'latitude']))]
    if not scenic_info['loc']:
        scenic_info['loc'] = [clean_data(judgment(['baiduData', 'longitude'])),
                              clean_data(judgment(['baiduData', 'latitude']))]

    scenic_info['loc'] = [
        scenic_info['loc'][0], scenic_info['loc'][1]]
    scenic_info['country'] = clean_data(judgment(['placeCountry']))
    scenic_info['googleData'] = clean_data(judgment(['googleData']))
    scenic_info['baiduData'] = clean_data(judgment(['baiduData']))
    if judgment('openTimes'):
        del data['openTimes'][0]['openTimeInfo']
        scenic_info['openTimes'] = clean_data(data['openTimes'])

    scenic_info['name'] = clean_data(judgment(['scenicName']))

    products_info = self.loc['menpiao_products'].find(
        {'placeId': str(scenic_id)},
        {'_id': 0, 'productTheme': 1, 'images': 1}
    )

    scenic_info['theme'] = []
    for product_info in products_info:
        scenic_info['theme'].extend(product_info['productTheme'])
        if product_info['images']:
            scenic_info['pic'] = product_info['images'][0]
    self.loc['menpiao_scenic'].update_one(
        {'id': str(scenic_id)},
        {'$set': scenic_info},
        upsert=True
    )
    print(json.dumps(scenic_info, ensure_ascii=False, indent=2))
    return [json.dumps(scenic_info, ensure_ascii=False, indent=2), 'finish']


@app.task(base=lvmamaTask, bind=True, ignore_result=True, max_retries=3)
def miss_scenic_id(self):
    for product in self.loc['menpiao_products'].find({}, ['id', 'placeId']):
        data = self.loc['menpiao_scenic'].find_one(
            {'id': product['placeId']},
            {'_id': 0, 'id': 1}
        )
        if not data:
            scenic_info.delay(product['placeId'])
            print(product['id'], product['placeId'], 'miss')
    return 'ok'

if __name__ == "__main__":
    miss_scenic_id.delay()
