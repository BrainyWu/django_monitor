# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import time
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty

default_threads = 2 * cpu_count()


def get_split_list(t_list, n):
    """list for multithreading by generator"""
    return (t_list[i: i + n] for i in range(0, len(t_list), n))


def thread_pool_view(func=None, items_list=None, max_threads=default_threads, per_size=500,
                     generator=True, inner_generator=False, **kwargs):
    """

    :param func:
    :param items_list: 总数据列表
    :param max_threads: 线程并发数
    :param per_size: 每个线程平均分配执行数
    :param generator: 返回集合类型标记：生成器或者列表
    :param inner_generator: 返回集合元素类型标记：生成器或者列表
    :param kwargs:
    :return: list or generator
    """
    split_list = get_split_list(items_list, per_size)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        tasks = [executor.submit(func, s_list, **kwargs) for s_list in split_list]

        if not inner_generator:
            result = (future.result() for future in as_completed(tasks))
        else:
            result = (list(future.result()) for future in as_completed(tasks))
        if not generator:
            result = sum(result, [])
    return result
