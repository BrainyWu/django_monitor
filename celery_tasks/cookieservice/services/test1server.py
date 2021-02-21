# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import random

from cookieservice.services.base_service import BaseService


class Test1LoginService(BaseService):
    name = "test1"

    def __init__(self, settings):
        # 从对应服务中随机选中一个user
        self.username = random.choice(settings[self.name]["users"])["username"]
        self.password = random.choice(settings[self.name]["users"])["password"]

    def check_login(self):
        pass

    def check_cookie(self, cookie_dict):
        pass

    def login(self):
        cookie_dict = {"test1": "test1"}
        return cookie_dict


if __name__ == "__main__":
    pass
