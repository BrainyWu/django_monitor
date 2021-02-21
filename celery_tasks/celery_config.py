# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from celery.schedules import crontab

broken_url = "redis://192.168.19.99:6379/5"  # 存储任务队列
backen_url = "redis://192.168.19.99:6379/6"  # 存储任务结果

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
worker_hijack_root_logger = False
result_expires = 60 * 60 * 12  # 过期时间设置

imports = [
    "celery_tasks.beat_tasks",  # 导入任务py文件
]

beat_schedule = {
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
