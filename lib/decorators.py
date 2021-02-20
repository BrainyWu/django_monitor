# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import threading


def callback(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args)
        t.start()
        # t.join()
    return wrapper()
