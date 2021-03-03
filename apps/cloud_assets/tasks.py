# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from celery import shared_task
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from lib.mysqldatabase import dbpool


@shared_task
def update_vm_assets():
    pass


@shared_task
def update_phy_assets():
    pass
