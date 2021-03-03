# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from celery import shared_task
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from cookieservice.server import cookie_srv


# 模拟登陆，获取cookie数据到redis中
@shared_task
def get_cookies():
    task_list = []
    login_executor = ThreadPoolExecutor(max_workers=5)
    for srv in cookie_srv.service_list:
        task = login_executor.submit(partial(cookie_srv.get_cookie_service, srv))
        task_list.append(task)

    # for future in as_completed(task_list):
    #     data = future.result()
    #     print(data)


@shared_task
def check_cookies():
    task_list = []
    check_executor = ThreadPoolExecutor(max_workers=5)
    for srv in cookie_srv.service_list:
        task = check_executor.submit(partial(cookie_srv.check_cookie_service, srv))
        task_list.append(task)
