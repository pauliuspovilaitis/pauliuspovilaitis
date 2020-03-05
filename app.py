#!/usr/bin/python
import cx_Oracle
import os
import sys
import config
from flask import Flask, jsonify, request

app = Flask(__name__)
os.environ['PATH'] = config.ENV_CONFIG['path']

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'data': str('wrong URL')})
       
@app.route('/pf/<dbTable>', methods=['GET'])
def pf(dbTable):
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
                    
@app.route('/sys2k/<dbTable>', methods=['GET'])        
def sys2k(dbTable):
    connection = None    
    try:    
        connection = cx_Oracle.connect(config.DATABASE_CONFIG_SYS2K['user'], 
                                       config.DATABASE_CONFIG_SYS2K['password'], 
                                       config.DATABASE_CONFIG_SYS2K['host'])
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