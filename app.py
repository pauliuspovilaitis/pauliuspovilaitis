#!/usr/bin/python

import os
from datetime import datetime
import cx_Oracle
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
import config
import socket

app = Flask(__name__)
os.environ['PATH'] = config.ENV_CONFIG['path']

handler = RotatingFileHandler(config.ENV_LOG['path'], maxBytes=1000000, backupCount=5)
handler.setLevel(logging.WARNING)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', None, "%"))
logger = logging.getLogger()
logger.addHandler(handler)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

tables = ['products',
          'melting_codes',
          'coatings',
          'edge_types',
          'finishes',
          'dual']


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': str('wrong URL')})


@app.route('/pf/<dbtable>', methods=['GET'])
def pf(dbtable):
    if dbtable not in tables:
        return jsonify({'error': 'table not allowed'})
    user = request.headers.get('user')
    connection = None    
    try:    
        connection = cx_Oracle.connect(config.DATABASE_CONFIG_PF['user'], 
                                       config.DATABASE_CONFIG_PF['password'], 
                                       config.DATABASE_CONFIG_PF['host'])
        cur = connection.cursor()
        result = cur.execute(f"""SELECT * FROM {dbtable}""")
        items = [dict(zip([key[0] for key in cur.description], row)) for row in result]
        cur.close()
        connection.close()    
        return jsonify({'data': items})  
    except Exception as e:  
        return jsonify({'error': str(e)})


@app.route('/sys2k/<dbtable>', methods=['GET'])
def sys2k(dbtable):
    if dbtable not in tables:
        return jsonify({'error': 'table not allowed'})
    user = request.headers.get('user')
    connection = None    
    try:    
        connection = cx_Oracle.connect(config.DATABASE_CONFIG_SYS2K['user'], 
                                       config.DATABASE_CONFIG_SYS2K['password'], 
                                       config.DATABASE_CONFIG_SYS2K['host'])
        cur = connection.cursor()
        result = cur.execute(f"""SELECT * FROM {dbtable}""")
        items = [dict(zip([key[0] for key in cur.description], row)) for row in result]
        cur.close()
        connection.close()    
        return jsonify({'data': items})  
    except Exception as e:  
        return jsonify({'error': str(e)})


@app.route('/test', methods=['GET'])
def test():
    user = request.headers.get('user')
    if not user:
        return jsonify({'error': 'wrong user'})
    app.logger.warning(' GET /test ' + str(user) + ' ' + hostname + ' ' + ip)
    return jsonify({'data': user})


if __name__ == '__main__':
   app.run(debug=True)