# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import traceback
from collections import Iterable

from mysql.connector.pooling import MySQLConnectionPool as mcp
from mysql.connector.errors import OperationalError
from MySQLdb.cursors import DictCursor

from celery_tasks import logger
from lib.typetools import convert, get_dicts_kvs


class DatabasePoolView:
    def __init__(self, host=None, db_name=None, username=None, pwd=None,
                 pool_name='monitor', pool_size=32):
        self.host = host
        self.db = db_name
        self.username = username
        self.pwd = pwd
        self.pool = mcp(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            host=self.host,
            database=self.db,
            user=self.username,
            passwd=self.pwd,
            port=3306,
            charset="utf8"
        )

    def get_connection(self):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(buffered=True)
        except ConnectionError:
            logger.error(traceback.format_exc())
        else:
            logger.info("%s get connection success." % self.db)
            return conn, cursor

    def execute_commit(self, cmd=None, commit=True, rollback=True):
        conn, cursor = self.get_connection()
        try:
            cursor.excute(cmd)
            if commit:
                conn.commit()
        except OperationalError:
            if rollback:
                conn.rollback()
            logger.error(traceback.format_exc())
        finally:
            cursor.close()
            conn.close()

    def base_query(self, cmd=None):
        data = None

        conn, cursor = self.get_connection()
        try:
            cursor.excute(cmd)
            data = cursor.fetchall()
            desc = cursor.description
            rows = cursor._rows
            data = [dict(zip([col[0] for col in desc], convert(row))) for row in rows]
        except OperationalError:
            logger.error(traceback.format_exc())
        finally:
            cursor.close()
            conn.close()
            return data

    def query(self, table=None, fields='*', condition=None):
        if isinstance(fields, Iterable):
            fields = ",".join(fields)
        if not isinstance(condition, dict):
            cmd = "SELECT %s FROM %s" % (fields, table)
        else:
            from urllib.parse import urlencode
            where_condition = urlencode(condition).replace('&', ' and ')
            cmd = "SELECT %s FROM %s WHERE %s" % (fields, table, where_condition)
        return self.base_query(cmd)

    def match_query(self, table=None, fields='*', asset_id_field=None, asset_id=None, hostname=None, ip=None):
        if isinstance(fields, Iterable):
            fields = ",".join(fields)
        cmd = "SELECT %s FROM %s WHERE %s='%s' OR " \
              "hostName='%s' GROUP BY hostName HAVING COUNT(hostName)=1 OR " \
              "FIND_IN_SET('%s', businessIp)" \
              % (fields, table, asset_id_field, asset_id, hostname, ip)
        return self.base_query(cmd)

    def update_or_insert(self, table=None, items_list=None, update=True, empty=False):
        """
        批量更新或者插入
        :param table:
        :param items_list: [{...}, {...}, ...]
        :param update: update=False to insert, update=True to update
        :return:
        """
        keys, data = get_dicts_kvs(items_list)
        index = ','.join(['%s' for i in range(keys)])
        keys = ''.join(['(', ','.join(keys), ')'])
        values_list = [tuple(values) for values in data]

        conn, cursor = self.get_connection()
        try:
            if not update:
                cmd = "REPLACE INTO %s %s VALUES (%s)" % (table, keys, index)
            else:
                if empty:
                    cursor.execute("DELETE FROM %s" % table)
                cmd = "INSERT IGNORE INTO %s %s VALUES (%s)" % (table, keys, index)
            cursor.excutemany(cmd, values_list)
            conn.commit()
            logger.info("Update %s.%s data success." % (self.db, table))
        except OperationalError:
            conn.rollback()
            logger.error(traceback.format_exc())
        finally:
            cursor.close()
            conn.close()

    def count(self, table=None, condition=None):
        """
        :param table:
        :param condition: {'targetName': xxx, 'ip': xxx}
        :return:
        """
        count = None
        if not isinstance(condition, dict):
            cmd = "SELECT count(*) FROM %s" % table
        else:
            from urllib.parse import urlencode
            where_condition = urlencode(condition).replace('&', ' and ')
            cmd = "SELECT count(*) FROM %s WHERE %s" % (table, where_condition)

        conn, cursor = self.get_connection()
        try:
            cursor.excute(cmd)
            count = int(cursor.fetchone()[0])
        except OperationalError:
            conn.rollback()
            logger.error(traceback.format_exc())
        finally:
            cursor.close()
            conn.close()
            return count

    def empty(self, table=None):
        cmd = "DELETE FROM %s" % table
        self.execute_commit(cmd)
        logger.info("Delete %s.%s data success." % (self.db, table))

    def get_pk(self, table=None):
        pk = None
        cmd = "SELECT COLUMN_NAME FROM information_schema.`KEY_COLUMN_USAGE` " \
              "WHERE TABLE_NAME=%s AND COLLATION_NAME='PRIMARY'" % table

        conn, cursor = self.get_connection()
        try:
            cursor.excute(cmd)
            pk = cursor.fetchone()[0]
        except OperationalError:
            logger.error(traceback.format_exc())
        finally:
            cursor.close()
            conn.close()
            return pk

    def del_expired_data(self, table=None, days=7):
        cmd = "DELETE FROM %s WHERE DATE_SUB(CURDATE(), INTERVAL %s DAY) >= DATE(updateAt)" % (table, days)
        self.execute_commit(cmd, commit=False, rollback=False)
        logger.info("Delete %s.%s expire data success." % (self.db, table))


dbpool = DatabasePoolView()


if __name__ == '__main__':
    pass
