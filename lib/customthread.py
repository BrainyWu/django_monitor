# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import logging
import threading

logger = logging.getLogger()


class CustomThread(threading.Thread):
    def __init__(self, func, args=(), **kwargs):
        super(CustomThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.func(*self.args, self.kwargs)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            logger.error(e)
