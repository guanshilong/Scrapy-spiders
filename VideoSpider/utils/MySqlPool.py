import pymysql
from DBUtils.PooledDB import PooledDB


class MySqlPool(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            db_config = {
                'host': '192.168.157.99',
                'port': 3306,
                'user': 'root',
                'passwd': 'root',
                'db': 'scrapy',
                'charset': 'utf8'
            }
            cls.pool = PooledDB(pymysql, maxconnections=20, setsession=['SET AUTOCOMMIT = 0'], **db_config)
            cls._instance = super(MySqlPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def getConn():
    # 必须在MySqlPool中实现单例,每次MySqlPool()都会调用__new__,会源源不断创建pool
    return MySqlPool().pool.connection()
    pass
