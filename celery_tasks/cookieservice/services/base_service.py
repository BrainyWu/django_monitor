# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import abc

from selenium import webdriver


# 继承BaseService必须实现login和check_cookie两个方法
class BaseService(metaclass=abc.ABCMeta):
    # 1. 第一种解决方案： 在父类的方法中抛出异常
    # 2. 第二种解决方案： 使用抽象基类

    def __init__(self, settings):
        self.driver = webdriver.Chrome("C:\Python37\chromedriver.exe")

    # def login(self):
    #     raise NotImplementedError

    @abc.abstractmethod
    def login(self):
        pass

    @abc.abstractmethod
    def check_cookie(self, cookie_dict):
        pass

