# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from celery_tasks import celery_app, logger
from cookieservice.settings import COOKIE_SERVICES
from cookieservice.server import CookieServer
from lib.mysqldatabase import DatabasePoolView

dbpool = DatabasePoolView()
cookie_srv = CookieServer(COOKIE_SERVICES)


@celery_app.task
def update_vm_assets():
    pass


@celery_app.task
def update_phy_assets():
    pass


# 模拟登陆，获取cookie数据到redis中
@celery_app
def get_cookies():
    task_list = []
    login_executor = ThreadPoolExecutor(max_workers=5)
    for srv in cookie_srv.service_list:
        task = login_executor.submit(partial(cookie_srv.get_cookie_service, srv))
        task_list.append(task)

    # for future in as_completed(task_list):
    #     data = future.result()
    #     print(data)


@celery_app
def check_cookies():
    task_list = []
    check_executor = ThreadPoolExecutor(max_workers=5)
    for srv in cookie_srv.service_list:
        task = check_executor.submit(partial(cookie_srv.check_cookie_service, srv))
        task_list.append(task)
