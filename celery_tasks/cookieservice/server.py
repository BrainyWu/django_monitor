# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import json

from django_redis import get_redis_connection

from celery_tasks import logger


class CookieServer:
    def __init__(self, cookies_setting):
        self.redis_cli = get_redis_connection("cookie")
        self.cookie_services = cookies_setting
        # 获取settings中服务类名
        self.service_list = [service['server_cls'] for service in self.cookie_services]

    def get_cookie_service(self, service):
        srv_cli = service(self.cookie_services)
        srv_name = srv_cli.name
        # 扫描cookie池中的数量不超过max_cookie_nums
        cookie_nums = self.redis_cli.scard(self.cookie_services[srv_name]["cookie_key"])
        if cookie_nums < self.cookie_services[srv_name]["max_cookie_nums"]:
            cookie_dict = srv_cli.login()
            self.redis_cli.sadd(self.cookie_services[srv_name]["cookie_key"], json.dumps(cookie_dict))
        else:
            logger.warning("%s服务的cookie池已满." % srv_name)

    def check_cookie_service(self, service):
        # 定时检查cookie的有效性
        srv_cli = service(self.cookie_services)
        srv_name = srv_cli.name
        all_cookies = self.redis_cli.smembers(self.cookie_services[srv_name]["cookie_key"])
        logger.info("%s服务目前可用cookie数量: %s" % (srv_name, len(all_cookies)))
        for cookie_str in all_cookies:
            cookie_dict = json.loads(cookie_str)
            valid = srv_cli.check_cookie(cookie_dict)
            if not valid:
                logger.debug("cookie: %s已经失效， 删除cookie" % cookie_dict)
                self.redis_cli.srem(self.cookie_services[srv_name]["cookie_key"], cookie_str)
        # 检查完之后重新设置过期时间
        expire_time = self.cookie_services[srv_name]["expiry"]
        self.redis_cli.expire(self.cookie_services[srv_name]["cookie_key"], expire_time)


if __name__ == '__main__':
    pass
