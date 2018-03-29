# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
# Broker and Backend
broker_url = 'pyamqp://guest@localhost//'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
timezone = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'
# import
imports = (
    'celery_app.task1',
    'celery_app.spider_cinema_film',
    'celery_app.komovie_cinema_film',
    'celery_app.lvmama_image',
)

task_annotations = {
    'celery_app.task1.hotel_ids_message_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.hotel_ids_rateplans_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.city_get_full_hotel_ids': {'rate_limit': '30/m'},
    'celery_app.task1.get_hotel_info_increment': {'rate_limit': '5000/m'}
}

task_time_limit = 60 * 10

beat_schedule = {
    'add-every-600-seconds': {
        'task': 'celery_app.task1.update_hotel',
        'schedule': crontab(hour=4, minute=30),       # 每 30 分钟执行一次
        'options': {'queue': "xiecheng_tasks"}          # 配置队列
    },
    'spider-city_id_fetch-every-1-day': {
        'task': 'celery_app.spider_cinema_film.city_id_fetch',
        'schedule': crontab(hour=2, minute=30),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
    'spider-cinema_id_fetch-every-1-day': {
        'task': 'celery_app.spider_cinema_film.cinema_id_fetch',
        'schedule': crontab(hour=2, minute=33),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
    'spider-datas_cleanse-every-1-day': {
        'task': 'celery_app.spider_cinema_film.datas_cleanse',
        'schedule': crontab(hour=3, minute=0),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
    'komovie-city_id_fetch-every-1-day': {
        'task': 'celery_app.komovie_cinema_film.city_id_fetch',
        'schedule': crontab(hour=2, minute=45),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
    'komovie-datas_cleanse-every-1-day': {
        'task': 'celery_app.komovie_cinema_film.datas_cleanse',
        'schedule': crontab(hour=3, minute=0),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
}
