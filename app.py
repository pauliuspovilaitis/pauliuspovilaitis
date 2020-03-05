#!/usr/bin/python
import cx_Oracle
import os
import sys
import config
from flask import Flask, jsonify, request

app = Flask(__name__)
os.environ['PATH'] = config.ENV_CONFIG['path']

@app.route('/pf/<dbTable>', methods=['GET'])
def index(dbTable):
    connection = None    
    try:    
        connection = cx_Oracle.connect(config.DATABASE_CONFIG_PF['user'], 
                                       config.DATABASE_CONFIG_PF['password'], 
                                       config.DATABASE_CONFIG_PF['host'])
        cur = connection.cursor()
        result = cur.execute(f"""SELECT * FROM {dbTable}""")
        items = [dict(zip([key[0] for key in cur.description], row )) for row in result]
        cur.close()
        connection.close()    
        return jsonify({'data': items})  
    except Exception as e:  
        return jsonify({'data': str(e)}) 
      
if __name__ == '__main__':
   app.run(debug=False)