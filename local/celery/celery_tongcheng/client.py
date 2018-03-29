# -*- coding: utf-8 -*-
from celery_app import task1
# task1.token_fetch.delay()
# task1.citys_fetch.delay()
task1.update_hotel.delay()
