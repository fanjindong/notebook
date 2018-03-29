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
    'celery_app.task'
)

CELERY_ANNOTATIONS = {
    'celery_app.task.scenic_info': {'rate_limit': '30/m'},
}

CELERYD_TASK_TIME_LIMIT = 60
