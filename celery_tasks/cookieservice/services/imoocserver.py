# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import time
import random

import requests

from celery_tasks import logger
from cookieservice.services.base_service import BaseService


class ImoocLoginService(BaseService):
    name = "imooc"

    def __init__(self, settings):
        super(ImoocLoginService, self).__init__(settings)
        # 从对应服务中随机选中一个user
        self.username = random.choice(settings[self.name]["users"])["username"]
        self.password = random.choice(settings[self.name]["users"])["password"]

    def check_login(self):
        try:
            self.driver.find_element_by_xpath("//*[@id ='header-user-card']")
            return True
        except Exception as e:
            logger.warning("%s login fail!" % self.name)

    def check_cookie(self, cookies_dict):
        pass

    def login(self):
        cookie_dict = {}
        try:
            self.driver.maximize_window()  # 将窗口最大化防止定位错误
        except Exception as e:
            pass

        self.driver.get("https://www.imooc.com/user/newlogin")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@name='email']").send_keys(self.username)
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys(self.password)
        self.driver.find_element_by_xpath("//*[@id='signup-form']//*[@type='button']").click()
        time.sleep(3)

        if self.check_login():
            cookie_dict = self.driver.get_cookie("imooc_uuid")
        self.driver.close()
        return cookie_dict


if __name__ == "__main__":
    from celery_tasks.cookieservice.settings import COOKIE_SERVICES
    imooc = ImoocLoginService(COOKIE_SERVICES)
    imooc.login()

