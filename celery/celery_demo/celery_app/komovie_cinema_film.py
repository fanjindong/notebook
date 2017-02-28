from __future__ import absolute_import, unicode_literals

import hashlib
import json
import operator
import time
import traceback
import urllib
from pprint import pprint

import redis
import requests
from celery import Task
from pymongo import MongoClient, ReturnDocument

from celery_app import app


class KoudianyingTask(Task):
    # 本地部署，所有和mongo、redis建立链接参数改变
    abstract = True
    _loc = None
    _pro = None  # 生产只可读
    _prow = None  # 生产可读写
    _stg = None
    _dev = None
    _rdb = None

    @property
    def loc(self):
        if self._loc is None:
            _loc = MongoClient('mongodb://localhost:27017')
            self._loc = _loc["boluome"]
        return self._loc

    @property
    def rdb(self):
        if self._rdb is None:
            self._rdb = redis.StrictRedis(
                host='127.0.0.1',
                port='6379',
                db=0,
                charset="utf-8",
                decode_responses=True
            )
        return self._rdb

    @property
    def pro(self):
        if self._pro is None:
            _pro = MongoClient(
                'mongodb://mongoc:Boluome123@139.198.1.168:10017/')
            self._pro = _pro["boluome"]
        return self._pro

    @property
    def prow(self):
        if self._prow is None:
            _prow = MongoClient(
                'mongodb://mongoc:Boluome123@139.198.1.168:10018/')
            self._prow = _prow["boluome"]
        return self._prow

    @property
    def stg(self):
        if self._stg is None:
            _stg = MongoClient(
                'mongodb://mongoc:Boluome123@139.198.1.168:12017/')
            self._stg = _stg["boluome"]
        return self._stg

    @property
    def dev(self):
        if self._dev is None:
            _dev = MongoClient(
                'mongodb://root:Boluome123@139.198.1.168:11017/')
            self._dev = _dev["boluome"]
        return self._dev

server = 'http://api.komovie.cn/movie/service'
channel_id = '189'
md5_key = 'GglrL3WIjp6CUZnj'


@app.task(base=KoudianyingTask, bind=True, ignore_result=True, max_retries=3)
def city_id_fetch(self):
    """获取城市列表，作为参数调用获取影院详细接口
    """
    city_list = set()
    action = 'city_Query'
    time_stamp = int(time.time() * 1000)
    hstr = urllib.request.quote(
        "{action}{time_stamp}{md5_key}".format(
            action=action,
            time_stamp=time_stamp,
            md5_key=md5_key
        )
    )
    enc = hashlib.md5(hstr.encode('utf-8')).hexdigest()

    post_data = {"action": action,
                 "time_stamp": time_stamp,
                 "enc": enc}
    headers = {"channel_id": channel_id}

    resp = requests.post(server,
                         headers=headers,
                         params=post_data)
    resp_data = resp.json()

    for item in resp_data['cities']:
        city_id = item['cityId']
        get_cinema_message_from_city_id.delay(city_id)

    return ['KoudianyingTask is Over!']


@app.task(base=KoudianyingTask, bind=True, ignore_result=True, max_retries=3)
def get_cinema_message_from_city_id(self, city_id):
    """传入参数城市ID,调用接口:通过城市获取影院列表,
       数据插入数据库dianying_cinema_kou,
       并调用get_movie_message_from_city_id()函数
    """
#     cinema_list = set()
    action = 'cinema_Query'
    time_stamp = int(time.time() * 1000)

    hstr = urllib.request.quote(
        "{action}{city_id}{time_stamp}{md5_key}".format(
            action=action,
            city_id=city_id,
            time_stamp=time_stamp,
            md5_key=md5_key
        )
    )
    enc = hashlib.md5(hstr.encode('utf-8')).hexdigest()

    post_data = {"action": action,
                 "city_id": city_id,
                 "time_stamp": time_stamp,
                 "enc": enc}
    headers = {"channel_id": channel_id}

    resp = requests.post(server,
                         headers=headers,
                         params=post_data)
    resp_data = resp.json()

    cinema_data = resp_data['cinemas']
    for cinema in cinema_data:
        #             cinema_list.add(cinema['cinemaId'])
        self.loc['dianying_cinema_kou'].update_one(
            {'cinemaId': cinema['cinemaId']},
            {'$set': cinema},
            upsert=True
        )
    get_movie_message_from_city_id.delay(city_id)
    return [city_id, 'all cinema insert is ok']


@app.task(base=KoudianyingTask, bind=True, ignore_result=True, max_retries=3)
def get_movie_message_from_city_id(self, city_id):
    """传入城市ID,遍历dianying_cinema_kou表所有影院ID,两者作为参数，
       调用接口：获取影院上映的影片列表，插入数据库，并返回
       get_movie_plans_from_cinema_id()函数"""
    cinema_ids = set()
    for cinema_id in self.loc['dianying_cinema_kou'].find({'cityId': city_id}, {'_id': 0, 'cinemaId': 1}):
        cinema_ids.add(cinema_id['cinemaId'])

    action = 'movie_Query'
    time_stamp = int(time.time() * 1000)

    hstr = urllib.request.quote(
        "{action}{city_id}{time_stamp}{md5_key}".format(
            action=action,
            city_id=city_id,
            time_stamp=time_stamp,
            md5_key=md5_key
        )
    )
    enc = hashlib.md5(hstr.encode('utf-8')).hexdigest()

    post_data = {
        "action": action,
        "city_id": city_id,
        "time_stamp": time_stamp,
        "enc": enc
    }
    headers = {"channel_id": channel_id}

    resp = requests.post(server,
                         headers=headers,
                         params=post_data)
    resp_data = resp.json()

    for cinema_id in cinema_ids:
        for item in resp_data['movies']:
            movie_id = item['movieId']

            self.loc['dianying_film_kou'].update_one(
                {'cinemaId': cinema_id, 'movieId': movie_id},
                {'$set': item},
                upsert=True
            )
            # print(cinema_id, movie_id, 'message insert is ok')
        get_movie_plans_from_cinema_id.delay(cinema_id)

    return [city_id, 'all film insert is ok']


@app.task(base=KoudianyingTask, bind=True, ignore_result=True, max_retries=3)
def get_movie_plans_from_cinema_id(self, cinema_id):
    """传入电影院ID,调用接口：查看排期列表,插入数据库"""
    action = 'plan_Query'
    ts = time.time()
    time_stamp = int(ts * 1000)

    plans_data = {}

    hstr = urllib.request.quote(
        "{action}{cinema_id}{time_stamp}{md5_key}".format(
            action=action,
            cinema_id=cinema_id,
            time_stamp=time_stamp,
            md5_key=md5_key
        )
    )
    enc = hashlib.md5(hstr.encode('utf-8')).hexdigest()

    post_data = {"action": action,
                 "cinema_id": cinema_id,
                 "time_stamp": time_stamp,
                 "enc": enc}
    headers = {"channel_id": channel_id}

    resp = requests.post(server, headers=headers, params=post_data)
    resp_data = resp.json()

    for item in resp_data.get('plans', []):
        plans_data.setdefault(item['movieId'], [])
        item.pop('cinema', None)
        item.pop('movie', None)
        plans_data[item['movieId']].append(item)

    today = time.strftime("%Y-%m-%d", time.localtime())
    for movie_id, movie_plans in plans_data.items():
        self.loc['dianying_film_kou'].update_one(
            {'cinemaId': cinema_id, 'movieId': movie_id},
            {'$set': {'plans': movie_plans, 'updatedAt': today}},
            upsert=True
        )
        # print(cinema_id, movie_id, 'plans insert is ok')
    return [cinema_id, 'all plans insert is ok']


@app.task(base=KoudianyingTask, bind=True, ignore_result=True, max_retries=3)
def datas_cleanse(self):
    today = time.strftime("%Y-%m-%d", time.localtime())
    delete_count = 0
    delete_count += self.loc['dianying_film_kou'].find(
        {"updatedAt": None}).count()
    delete_count += self.loc['dianying_film_kou'].find(
        {"updatedAt": {"$lt": today}}).count()
    self.loc['dianying_film_kou'].delete_many({"updatedAt": None})
    self.loc['dianying_film_kou'].delete_many({"updatedAt": {"$lt": today}})
    return ['delete count is', delete_count]
