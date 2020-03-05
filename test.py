#!/usr/bin/python
import cx_Oracle
import os
import sys
import config
import json

connection = None
try:
    os.environ['PATH'] = config.ENV_CONFIG['path']
    connection = cx_Oracle.connect(config.DATABASE_CONFIG_SYS2K['user'], 
                                   config.DATABASE_CONFIG_SYS2K['password'], 
                                   config.DATABASE_CONFIG_SYS2K['host'])
    cur = connection.cursor()
    cur.execute("SELECT CURRENT_TIMESTAMP FROM DUAL")
    col = cur.fetchone()[0]
    print(col)
    cur.close()
    connection.close()
except cx_Oracle.Error as error:
    print(str(error))


