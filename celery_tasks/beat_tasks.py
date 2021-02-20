# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from celery_tasks import celery_app
from lib.mysqldatabase import DatabasePoolView

dbpool = DatabasePoolView()


@celery_app.task
def update_vm_assets():
    pass


@celery_app.task
def update_phy_assets():
    pass
