
# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
import hashlib
import json
import time
import traceback

import redis
import requests
from celery import Task
from pymongo import MongoClient, ReturnDocument

from celery_app import app


class LvmamaTask(Task):
    # 本地部署，所有和mongo、redis建立链接参数改变
    abstract = True
    _loc = None
    _pro = None  # 生产只可读
    _stg = None
    _dev = None

    @property
    def loc(self):
        if self._loc is None:
            _loc = MongoClient('mongodb://localhost:27017')
            self._loc = _loc["boluome"]
        return self._loc

    @property
    def pro(self):
        if self._pro is None:
            _pro = MongoClient(
                'mongodb://mongoc:Boluome123@139.198.1.168:10017/')
            self._pro = _pro["boluome"]
        return self._pro

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


@app.task(base=LvmamaTask, bind=True, ignore_result=True, max_retries=3)
def pic_url_fetch(self):
    for item in self.stg.menpiao_scenic.find({}, {'id': 1, 'pic': 1, '_id': 0}):
        url = item.get('pic', '')
        if not url:
            continue
        image_url_down.apply_async(args=[url])
    return 'ok'


@app.task(base=LvmamaTask, bind=True, ignore_result=True, max_retries=3)
def image_url_fetch(self):
    for item in self.stg.menpiao_products.find({}, {'id': 1, 'images': 1, '_id': 0}):
        url_list = item.get('images', [])
        if not url_list:
            continue
        for url in url_list:
            image_url_down.apply_async(args=[url])
    return 'ok'


@app.task(base=LvmamaTask, bind=True, ignore_result=True, max_retries=3)
def image_url_down(self, url):
    image_format = url.split('.')[-1]
    hstr = hashlib.md5(url.encode()).hexdigest()
    p1 = int(hstr[:3], 16) // 4
    p2 = int(hstr[3:6], 16) // 4
    os.system("mkdir -p /tmp/{}/{}".format(p1, p2))
    os.system("wget {} -O /tmp/{}/{}/{}.{} -q".format(url, p1, p2, hstr, image_format))
    return 'down ok'
