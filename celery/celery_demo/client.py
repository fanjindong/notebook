# -*- coding: utf-8 -*-
from celery_app import task1
from celery_app import spider_cinema_film

# task1.token_fetch.delay()
# task1.full_citys_fetch.delay()
# task1.update_hotel.delay()

spider_cinema_film.city_id_fetch.delay()
spider_cinema_film.cinema_id_fetch.delay()
