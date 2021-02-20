# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import traceback

import pandas as pd
from sqlalchemy import create_engine

from celery_tasks import logger


class PandasDatabaseView:
    def __init__(self, host=None, db_name=None, username=None, pwd=None):
        self.host = host
        self.db = db_name
        self.username = username
        self.pwd = pwd
        self.conn = self.connect()

    def connect(self):
        return create_engine("mysql+pymysql://{0}:{1}@{2}:3306/{3}".format(
                             self.username, self.pwd, self.host, self.db), encoding="utf-8")

    def query(self, table=None, fields='*', condition=None, frame=True):
        if not isinstance(condition, dict):
            cmd = "SELECT %s FROM %s" % (fields, table)
        else:
            from urllib.parse import urlencode
            where_condition = urlencode(condition).replace('&', ' and ')
            cmd = "SELECT %s FROM %s WHERE %s" % (fields, table, where_condition)

        df = pd.read_sql_query(cmd, con=self.conn)
        if frame:
            return df
        else:
            return df.to_dict("records")

    def empty(self, table=None):
        cmd = "DELETE FROM %s" % table
        self.conn.execute(cmd)
        logger.info("Delete %s.%s data success." % (self.db, table))
