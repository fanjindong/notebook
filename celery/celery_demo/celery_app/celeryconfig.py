# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
# Broker and Backend
BROKER_URL = 'pyamqp://guest@localhost//'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'
# import
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.spider_cinema_film'
)

CELERY_ANNOTATIONS = {
    'celery_app.task1.hotel_ids_message_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.hotel_ids_rateplans_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.city_get_full_hotel_ids': {'rate_limit': '30/m'},
    'celery_app.task1.get_hotel_info_increment': {'rate_limit': '5000/m'}
}

CELERYD_TASK_TIME_LIMIT = 60 * 3

CELERYBEAT_SCHEDULE = {
    # 'add-every-600-seconds': {
    #     'task': 'celery_app.task1.update_hotel',
    #     'schedule': timedelta(seconds=60 * 30),       # 每 30 分钟执行一次
    #  'options': {'queue': "schedule"}          # 配置队列
    # },
    'add-every-1-day': {
        'task': 'celery_app.spider_cinema_film.city_id_fetch',
        'schedule': crontab(hour=19, minute=40),       # 每 天 执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    },
    'add-every-1-day': {
        'task': 'celery_app.spider_cinema_film.cinema_id_fetch',
        'schedule': crontab(hour=19, minute=43),       # 每 天 分钟执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    }
}
