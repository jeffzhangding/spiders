__author__ = 'jeff'

from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool


class PostgresqlConnection:
    def __init__(self, **kwargs):
        self.pool = ThreadedConnectionPool(minconn=kwargs['minconn'], maxconn=kwargs['maxconn'],
                                           database=kwargs['database'], user=kwargs['username'],
                                           password=kwargs['password'], host=kwargs['host'], port=kwargs['port'])

    @contextmanager
    def cursor(self, auto_commit=True):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            if auto_commit:
                conn.commit()
            if cursor is not None and not cursor.closed:
                cursor.close()
            self.pool.putconn(conn)

    def close(self):
        self.pool.closeall()


class PostgresqlTool(object):
    """工具"""

    @classmethod
    def get_dict(cls, cr):
        """获取字典类型的数据"""
        res = cr.fetchone()
        if res is None:
            return {}
        else:
            head = [i[0] for i in cr.description]
            return dict(zip(head, res))

    @classmethod
    def get_dicts(cls, cr):
        """获取字典类型的数据"""
        data = cr.fetchall()
        if data is None:
            return []
        else:
            head = [i[0] for i in cr.description]
            return [dict(zip(head, i)) for i in data]



