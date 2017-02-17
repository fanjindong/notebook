# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
# Broker and Backend
BROKER_URL = 'pyamqp://guest@localhost//'
#CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'
# import
CELERY_IMPORTS = (
    'celery_app.task1'
)

CELERY_ANNOTATIONS = {
    'celery_app.task1.hotel_ids_message_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.hotel_ids_rateplans_fetch': {'rate_limit': '100/m'},
    'celery_app.task1.city_get_full_hotel_ids': {'rate_limit': '30/m'},
    'celery_app.task1.get_hotel_info_increment': {'rate_limit': '5000/m'}
}

CELERYD_TASK_TIME_LIMIT = 60 * 3

CELERYBEAT_SCHEDULE = {
    'add-every-600-seconds': {
        'task': 'celery_app.task1.update_hotel',
        'schedule': timedelta(seconds=60 * 30),       # 每 30 分钟执行一次
        #  'options': {'queue': "schedule"}          # 配置队列
    }
}
