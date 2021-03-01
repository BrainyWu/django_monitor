# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import random

from cookieservice.services.base_service import BaseService


class Test2LoginService(BaseService):
    name = "test2"

    def __init__(self, settings):
        super(Test2LoginService, self).__init__(settings)
        self.username = random.choice(settings[self.name]["users"])["username"]
        self.password = random.choice(settings[self.name]["users"])["password"]

    def check_login(self):
        pass

    def check_cookie(self, cookie_dict):
        pass

    def login(self):
        cookie_dict = {"test2": "test2"}
        return cookie_dict


if __name__ == "__main__":
    pass











