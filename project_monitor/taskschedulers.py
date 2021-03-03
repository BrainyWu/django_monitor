# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from celery.schedules import crontab

# http://docs.jinkan.org/docs/celery/userguide/periodic-tasks.html
beat_schedulers = {
    "update_vm_assets": {
        "task": "xxx",
        "schedule": crontab(hour="*/1"),
        "args": ()
    },
    "get_cookies": {
        "task": "xxx",
        "schedule": crontab(day_of_week="0-6"),
        "args": ()
    },
    "check_cookies": {
        "task": "xxx",
        "schedule": crontab(day_of_week="0-6"),
        "args": ()
    },
}