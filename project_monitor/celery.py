# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_monitor.settings.base")

# 创建celery应用实例
app = Celery("celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
