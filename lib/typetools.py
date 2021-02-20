# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import collections
import datetime
import itertools


def convert(obj):
    """db data transfer to utf8"""
    if isinstance(obj, tuple):
        return (convert(item) for item in obj)
    else:
        try:
            obj = obj.decode("utf-8")
        except:
            pass
        return obj


def get_dicts_kvs(dicts):
    """get list dict keys and values"""
    keys = collections.OrderedDict(dicts[0].keys)
    values_list = [collections.OrderedDict(items).values() for items in dicts]
    return keys, values_list


def get_interval_time(t_start, t_end):
    """calculation of interval time"""
    start_time = datetime.datetime.strptime(t_start, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(t_end, "%Y-%m-%d %H:%M:%S")
    return (end_time - start_time).seconds


if __name__ == '__main__':
    import base64

    a = "wuhat1"
    b = base64.b64encode(a.encode())
    c = base64.b64decode(b).decode()
    print(a, b, c)
