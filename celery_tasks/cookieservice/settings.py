# -*- coding: utf-8 -*-
__author__ = 'wuhai'

from cookieservice.services import test1server, test2server

# 各个网站的登陆账号信息
COOKIE_SERVICES = {
    "test1": {
        "server_cls": test1server,  # 服务登陆类名
        "cookie_key": "zhihu:cookies",  # redis key
        "max_cookie_nums": 10,  # cookie池最大容量
        "expiry": 30,  # set过期时间， 最好定时任务执行的间隔<过期时间，避免定时任务没有执行，cookies全部过期
        "users": [
            {
                "username": "18xxxxxxxxx",
                "password": "admin123",
            }
        ]
    },
    "test2": {
        "server_cls": test2server,
        "cookie_key": "bili:cookies",
        "max_cookie_nums": 10,
        "expiry": 30,
        "users": [
            {
                "username": "18xxxxxxxxx",
                "password": "admin123",
            }
        ]
    }
}
