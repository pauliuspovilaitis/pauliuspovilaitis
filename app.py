#!/usr/bin/python
import cx_Oracle
import os
import sys
import config
from flask import Flask, jsonify, request

app = Flask(__name__)
os.environ['PATH'] = config.ENV_CONFIG['path']

@app.route('/sys2k/gettime', methods=['GET'])
def index():
    connection = None     
    connection = cx_Oracle.connect(config.DATABASE_CONFIG_SYS2K['user'], 
                                   config.DATABASE_CONFIG_SYS2K['password'], 
                                   config.DATABASE_CONFIG_SYS2K['host'])
    cur = connection.cursor()
    cur.execute("SELECT CURRENT_TIMESTAMP FROM DUAL")
    col = cur.fetchone()[0]   
    cur.close()
    connection.close()    
    return jsonify({'data': col})  
    
    
if __name__ == '__main__':
   app.run(debug=True)