import cx_Oracle
import pymysql
import configparser
from log import logging


class DB(object):

    __filename = '/Users/zhouyongwei/vscode-workspace/kitbox/config/db.ini'

    def __init__(self, dbName):
        self.conn = None
        self.cursor = None
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(DB.__filename, encoding='utf-8')
        if dbName is None or dbName == '':
            self.dbName = config.get('DEFAULT', 'db')
            logging.info('选用默认数据库连接[%s]' % self.dbName)
        else:
            self.dbName = dbName
        self.type = config.get(self.dbName, 'type')
        self.prename = config.get(self.dbName, 'prename')
        self.__username = config.get(self.dbName, 'username')
        self.__password = config.get(self.dbName, 'password')
        self.__host = config.get(self.dbName, 'host')
        self.__port = config.getint(self.dbName, 'port')
        self.__sid = config.get(self.dbName, 'sid', fallback=None)
        self.__servicename = config.get(
            self.dbName, 'servicename', fallback=None)
        self.__db = config.get(self.dbName, 'db', fallback=None)

    def open(self):
        logging.info('打开数据库连接[{0}]'.format(str(self)))
        if self.type.lower() == 'mysql':
            self.conn = pymysql.connect(
                host=self.__host, port=self.__port, db=self.__db, user=self.__username, password=self.__password)
        elif self.type.lower() == 'oracle':
            if not self.__sid is None:
                dsn = cx_Oracle.makedsn(self.__host, self.__port, self.__sid)
            else:
                dsn = cx_Oracle.makedsn(
                    self.__host, self.__port, service_name=self.__servicename)
            self.conn = cx_Oracle.connect(self.__username, self.__password, dsn)
        else:
            error_message = 'NOT SUPPORT DBTYPE [{0}]'.format(self.type)
            logging.error(error_message)
            raise Exception(error_message)
        self.cursor = self.conn.cursor()
        logging.info('打开数据库连接成功')

    def close(self):
        try:
            if self.cursor:
                logging.info('关闭数据库游标[{0}]'.format(self.dbName))
                self.cursor.close()
            if self.conn:
                logging.info('关闭数据库连接[{0}]'.format(self.dbName))
                self.conn.close()
        except Exception as e:
            logging.info('关闭数据库异常', e)

    def __str__(self):
        return self.dbName+'::type={0},username={1},password={2},host={3}, port={4},sid={5}, servicename={6}, db={7}, prename={8}'\
            .format(self.type, self.__username, '*', self.__host, self.__port, self.__sid, self.__servicename, self.__db, self.prename)


if __name__ == '__main__':
    db = DB('MYBATIS')
    #db = DB(None)
    try:
        cursor = db.open()
    finally:
        db.close()
