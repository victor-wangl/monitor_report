# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      DBManager
    Description:    
    Author:         wanglin
    Date:           2018/1/3
--------------------------------------------
    Change Activity:2018/1/3;
--------------------------------------------
"""
__author__ = 'wanglin'

import os
import json
import cx_Oracle
import MySQLdb
from DBUtils.PooledDB import PooledDB
from util.ConfigHandler import ConfigHandler
from util.Singleton import Singleton
from util.LogHandler import LogHandler

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

log = LogHandler('DBManager')

class DBManager(object):
    __metaclass__ = Singleton

    def __init__(self, option='oracle'):
        self.option = option
        self.config = ConfigHandler().get(self.option)
        if option == 'oracle':
            dsn = '{host}:{port}/{db}'.format(host=self.config['host'], port=self.config['port'], db=self.config['db'])
            connKwargs = {'user': self.config['user'], 'password': self.config['passwd'], 'dsn': dsn}
            self._pool = PooledDB(cx_Oracle, mincached=2, maxcached=2, maxshared=5, maxconnections=10, **connKwargs)
        else:
            connKwargs = {'host': self.config['host'], 'port': int(self.config['port']), 'user': self.config['user'],
                          'passwd': self.config['passwd'], 'db': self.config['db'], 'charset': self.config['charset']}
            self._pool = PooledDB(MySQLdb, mincached=2, maxcached=2, maxshared=5, maxconnections=10, **connKwargs)

    def getConn(self):
        return self._pool.connection()


_dbManager = DBManager()

 tables = [{'table': 'TEST.PAYCUSTOMER', 'desc': u'客户信息表'},
           {'table': 'TEST.PAYUSER', 'desc': u'用户表'},
           # {'table': 'TEST.PAYJNLS', 'desc': u'手刷交易表'},
           {'table': 'TEST.PAYBINDBANKCARD2', 'desc': u'绑定卡表'},
           {'table': 'TEST.TM_APP_MAIN', 'desc': u'信审主表'},
           {'table': 'TEST.TM_APP_PRIM_APP_INFO', 'desc': u'申请人信息表'},
           {'table': 'TEST.TM_CONTRACT_LIST', 'desc': u'申请人通讯录表'},
           {'table': 'TEST.C_CALL_DETAILS', 'desc': u'申请人通话详单表'}, ]


def getConn():
    return _dbManager.getConn()


def selectSql(sql):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0]


def get_table_count():
    result = []
    for table in tables:
        sql = 'select count(1) from {tableName}'.format(tableName=table['table'])
        table['count'] = selectSql(sql)
        log.info(table)
        result.append(table)
    return json.dumps(result)


if __name__ == '__main__':
    get_table_count()
