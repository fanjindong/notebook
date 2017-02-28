
# coding: utf-8
from __future__ import absolute_import, unicode_literals

import hashlib
import json
import time
import traceback

import redis
import requests
from celery import Task
from pymongo import MongoClient, ReturnDocument

from celery_app import app


class ZhizhuwangTask(Task):
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

server = 'http://filmapi.spider.com.cn/v2/boluomi/'
app_key = 'boluomi'
app_secret = 'BV07RK5W9U3Z'


@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def city_id_fetch(self):
    """获取所有城市ID列表，调用cinema接口爬取每个城市电影院信息，存入mongo数据库
    """
    city_url = 'http://filmapi.spider.com.cn/v2/boluomi/cityList.html'
    resp = None
    hstr = "{}{}".format(app_key, app_secret)
    sign = hashlib.md5(hstr.encode('utf-8')).hexdigest()
    post_data = {"key": app_key,
                 "sign": sign,
                 "filetype": "json"}

    resp = requests.post(city_url, params=post_data)
    resp_data = resp.json()
    city_data = resp_data['data']

    for item in city_data:
        city_id = item['cityId']
        city_id_get_cinema_information.delay(city_id)
    return ['city_id_fetch function is ok']


@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def city_id_get_cinema_information(self, city_id):
    # cinema_list = set()
    cinema_url = 'http://filmapi.spider.com.cn/v2/boluomi/cinemaList.html'
    hstr = "{}{}{}".format(city_id, app_key, app_secret)
    sign = hashlib.md5(hstr.encode('utf-8')).hexdigest()
    post_data = {"key": app_key,
                 "cityId": city_id,
                 "sign": sign,
                 "filetype": "json"}

    resp = requests.post(cinema_url, params=post_data)
    resp_data = resp.json()
    cinema_data = resp_data['data']
    for cinema in cinema_data:
        # cinema_list.add(cinema['cinemaId'])
        self.loc['dianying_cinema_zzw'].update_one(
            {'cinemaId': cinema['cinemaId']}, {'$set': cinema}, upsert=True)
        # mc_stg.boluome.dianying_cinema_zzw.update_one(
        #     {'cinemaId': cinema['cinemaId']}, {'$set': cinema}, upsert=True)
        # mc_pro.boluome.dianying_cinema_zzw.update_one(
        #     {'cinemaId': cinema['cinemaId']}, {'$set': cinema}, upsert=True)
    return [city_id, 'is ok']
# dianying_cinema_zzw 数据表完成


# dianying_film_zzw 表

@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def cinema_id_fetch(self):
    """从mongo数据库dianying_cinema_zzw表中，拿取电影院ID：cinemaId，分别调用电影信息接口
    """
    ts = time.time()
    range_date = []
    for i in range(5):
        range_date.append(
            time.strftime("%Y-%m-%d", time.localtime(ts + 86400 * i))
        )

    for cinema in self.loc['dianying_cinema_zzw'].find({}, {'_id': 0, 'cinemaId': 1}):
        cinema_id = cinema['cinemaId']
        film_datas_fetch_and_pretreatment.delay(cinema_id)
        cinema_id_get_film_information.delay(cinema_id, range_date)

    return ['cinema_id_fetch function is ok']


@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def film_datas_fetch_and_pretreatment(self, cinema_id):
    """获取所有电影票的数据，并预处理
    """
    film_url = 'http://filmapi.spider.com.cn/v2/boluomi/filmList.html'
    film_id = ''
    hstr = "{}{}{}".format(film_id, app_key, app_secret)
    sign = hashlib.md5(hstr.encode('utf-8')).hexdigest()
    post_data = {"key": app_key,
                 "filmId": film_id,
                 "sign": sign,
                 "filetype": "json"}

    resp = requests.post(film_url, params=post_data)
    resp_data = resp.json()
    for item in resp_data['data']:
        film_id = item['filmId']
        self.loc['dianying_film_zzw'].update_one(
            {'filmId': film_id, 'cinemaId': cinema_id},
            {'$set': item},
            upsert=True
        )

    return [cinema_id, len(resp_data['data']), 'is ok']


@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def cinema_id_get_film_information(self, cinema_id, range_date):
    datas = {}
    for date in range_date:
        show_url = 'http://filmapi.spider.com.cn/v2/boluomi/showList.html'
        film_id = ''
        hstr = "{}{}{}{}{}".format(
            cinema_id, film_id, date, app_key, app_secret)
        sign = hashlib.md5(hstr.encode('utf-8')).hexdigest()
        post_data = {"key": app_key,
                     "cinemaId": cinema_id,
                     "filmId": film_id,
                     "showDate": date,
                     "sign": sign,
                     "filetype": "json"}

        resp = requests.post(show_url, params=post_data)
        resp_data = resp.json()
        show_data = resp_data['data']

        for item in show_data:
            film_id = item['filmId']
            datas.setdefault(film_id, [])
            datas[film_id].append(item)
    today = time.strftime("%Y-%m-%d", time.localtime())
    for key, value in datas.items():
        self.loc['dianying_film_zzw'].update_one(
            {'filmId': key, 'cinemaId': cinema_id},
            {'$set': {'plans': value, 'updatedAt': today}},
            upsert=True
        )
    return ['cinema_id:', cinema_id, 'is ok']


@app.task(base=ZhizhuwangTask, bind=True, ignore_result=True, max_retries=3)
def datas_cleanse(self):
    today = time.strftime("%Y-%m-%d", time.localtime())
    delete_count = 0
    delete_count += self.loc['dianying_film_zzw'].find(
        {"updatedAt": None}).count()
    delete_count += self.loc['dianying_film_zzw'].find(
        {"updatedAt": {"$lt": today}}).count()
    self.loc['dianying_film_zzw'].delete_many({"updatedAt": None})
    self.loc['dianying_film_zzw'].delete_many({"updatedAt": {"$lt": today}})
    return ['delete count is', delete_count]
