# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from collections import Iterable
import logging
import traceback
import threading

import asyncio
import aiomysql
from mysql.connector.errors import OperationalError

from lib.typetools import get_dicts_kvs

logger = logging.getLogger()


class AioMysqlPoolView:
    def __init__(self, host=None, user=None, password=None, db=None, pool_size=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.pool_size = pool_size
        self._lock = threading.Lock()
        self._pool = None

    def close_pool(self):
        with self._lock:
            if self._pool:
                self._pool.close()

    async def get_pool(self):
        if not self._pool:
            with self._lock:  # 保证多线程下拿到同一个连接池实例
                if not self._pool:
                    self._pool = await aiomysql.create_pool(
                        maxsize=self.pool_size,
                        host=self.host,
                        user=self.password,
                        password=self.password,
                        db=self.db,
                        charset="utf-8",
                        autocommit=True,
                    )
        return self._pool

    async def execute(self, cmd):
        pool = await self.get_pool()

        async with pool.acquire() as conn:
            async with conn.cusor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(cmd)
                    return await cursor.fetchall()
                except OperationalError:
                    logger.error(traceback.format_exc())

    async def query(self, table=None, fields='*', condition=None):
        if isinstance(fields, Iterable):
            fields = ",".join(fields)
        if not isinstance(condition, dict):
            cmd = "SELECT %s FROM %s" % (fields, table)
        else:
            from urllib.parse import urlencode
            where_condition = await urlencode(condition).replace('&', ' and ')
            cmd = "SELECT %s FROM %s WHERE %s" % (fields, table, where_condition)
        return await self.execute(cmd)

    async def update_or_insert(self, table=None, items_list=None, update=True, empty=False):
        keys, data = await get_dicts_kvs(items_list)
        index = ','.join(['%s' for i in range(keys)])
        keys = ''.join(['(', ','.join(keys), ')'])
        values_list = [tuple(values) for values in data]

        pool = await self.get_pool()

        async with pool.acquire() as conn:
            async with conn.cusor(aiomysql.DictCursor) as cursor:
                try:
                    if not update:
                        cmd = "REPLACE INTO %s %s VALUES (%s)" % (table, keys, index)
                    else:
                        if empty:
                            await cursor.execute("DELETE FROM %s" % table)
                        cmd = "INSERT IGNORE INTO %s %s VALUES (%s)" % (table, keys, index)
                    await cursor.excutemany(cmd, values_list)
                    await conn.commit()
                    logger.info("Update %s.%s data success." % (self.db, table))
                except OperationalError:
                    await conn.rollback()
                    logger.error(traceback.format_exc())

