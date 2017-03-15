from __future__ import absolute_import, unicode_literals

import time
from datetime import datetime, timedelta
import json
import psycopg2
from pymongo import MongoClient, ReturnDocument
from pymongo import DESCENDING

mc_stg = MongoClient(
    ["mongodb://root:Boluome123@192.168.2.3", "192.168.2.4"], replicaset="foba")
mc_pro = MongoClient(
    ["mongodb://root:Boluome123@192.168.1.6", "192.168.1.7"], replicaset="foba")
mc_dev = MongoClient(
    ["mongodb://root:Boluome123@192.168.0.7", "192.168.0.10"], replicaset="foba")

conn = psycopg2.connect(
    "host=192.168.0.8 dbname=oto_saas user=boluome password=Boluome123")
cur = conn.cursor()


def mdb_data_fetch(start, end, app_code='allinpay'):
    # count = mc_dev.boluome.order_lite_list.find({
    #     'appCode': app_code,
    #     'createdAt': {'$gte': start, '$lt': end}}
    # ).count()
    mdb_data = mc_dev.boluome.order_lite_list.find({
        'appCode': app_code,
        'createdAt': {'$gte': start, '$lt': end}}
    )
    return data_preprocessing(mdb_data)


def data_preprocessing(mdb_data):
    insert_data = {'all': {'amount': 0, 'number': 0, 'number_completed': 0}}
    for item in mdb_data:
        key = item['orderType'] + '_' + item['channel']
        insert_data.setdefault(key, {})
        insert_data[key].setdefault('amount', 0)
        insert_data[key][
            'amount'] += item['price'] if item['status'] in [3, 4] else 0
        insert_data['all'][
            'amount'] += item['price'] if item['status'] in [3, 4] else 0
        insert_data[key].setdefault('number', 0)
        insert_data[key]['number'] += 1
        insert_data['all']['number'] += 1
        insert_data[key].setdefault('number_completed', 0)
        insert_data[key][
            'number_completed'] += 1 if item['status'] in [3, 4] else 0
        insert_data['all'][
            'number_completed'] += 1 if item['status'] in [3, 4] else 0
    return insert_data


def hourly_update(now_time):
    now_time = now_time.split('-')
    start_time = time.mktime(
        (int(now_time[0]), int(now_time[1]), int(now_time[2]), int(now_time[3]) - 1, 0, 0, 0, 0, 0)) * 1000
    end_time = time.mktime(
        (int(now_time[0]), int(now_time[1]), int(now_time[2]), int(now_time[3]), 0, 0, 0, 0, 0)) * 1000
    insert_data = mdb_data_fetch(start_time, end_time)
    sql_update = ''
    for key, value in insert_data.items():
        sql_update += "UPDATE transaction_amount_daily \
            SET amount_hourly[{hour}]={0}, \
            number_of_completed_orders_hourly[{hour}]={1} \
            WHERE id='ceshi';".format(
            value['amount'],
            value['number_completed'],
            hour=int(now_time[3]) - 1
        )
    cur.execute(sql_update)
    # conn.commit()
    # conn.close()


def daily_insert(day_time, app_code='allinpay'):
    now_time = day_time.split('-')
    start_time = time.mktime(
        (int(now_time[0]), int(now_time[1]) - 1, int(now_time[2]), 0, 0, 0, 0, 0, 0)) * 1000
    end_time = time.mktime(
        (int(now_time[0]), int(now_time[1]), int(now_time[2]), 24, 0, 0, 0, 0, 0)) * 1000
    insert_data = mdb_data_fetch(start_time, end_time)
    sql_insert = ''
    for key, value in insert_data.items():
        sql_insert += "INSERT INTO transaction_amount_daily(id, check_date) \
            VALUES ('{}','{}');".format('-'.join([app_code, key, day_time]), day_time)
    cur.execute(sql_insert)
    # conn.commit()
    # conn.close()


def daily_update(day_time, app_code='allinpay'):
    now_time = day_time.split('-')
    start_time = time.mktime(
        (int(now_time[0]), int(now_time[1]), int(now_time[2]), 0, 0, 0, 0, 0, 0)) * 1000
    end_time = time.mktime(
        (int(now_time[0]), int(now_time[1]), int(now_time[2]), 24, 0, 0, 0, 0, 0)) * 1000
    insert_data = mdb_data_fetch(start_time, end_time)
    sql_update = ''
    for key, value in insert_data.items():
        sql_update += "UPDATE transaction_amount_daily \
            SET category={}, mtime='{}', app_id={}, app_code={},\
            amount={}, number_of_orders={}, number_of_completed_orders={},\
            WHERE id={};".format(
            key,
            # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            datetime.now(),
            149,
            app_code,
            value['amount'],
            value['number'],
            value['number_completed'],
            '-'.join([app_code, key, day_time])
        )
    cur.execute(sql_update)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    daily_insert('2017-03-01')
    for i in range(24):
        hourly_update('2017-03-01-{}-01-01'.format(i + 1))
