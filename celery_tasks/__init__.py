# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import logging

from celery import Celery

# 创建celery应用实例
celery_app = Celery("monitor_celery")
logger = logging.getLogger("celery")

celery_app.config_from_object("celery_tasks.celery_config")
