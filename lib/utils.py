# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from collections import Iterable
import re
from multiprocessing import cpu_count

ip_pattern = "[0-9]{1,3}\.[0-9{1,3}\.[0-9{1,3}\.[0-9{1,3}"


def get_cpu_count():
    return cpu_count()


def get_all_methods(obj=None):
    return [name for name in dir(obj) if hasattr(getattr(obj, name), name)]


def get_public_methods(obj):
    return [name for name in get_all_methods(obj) if name[0] != '_']


def custom_filter(func=None, seq=None):
    """自定义filter生成器"""
    if func is None:
        func = bool
    for item in seq:
        new_item = func(item)
        if new_item:
            yield new_item


def get_ip_list(ips):
    """
    :param ips:  iterable
    :return: ip list
    """
    if isinstance(ips, Iterable):
        ips = ','.join(ips)
    return re.findall(ip_pattern, ips)


def get_illegal_ips(ips):
    """获取非ip数据"""
    if isinstance(ips, str):
        ips = ips.split(',')
    return [ip for ip in ips if not re.match(ip_pattern, ip)]
