#!/usr/bin/python

import logging
import os
import socket
from logging.handlers import RotatingFileHandler
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



import cx_Oracle
from flask import Flask, jsonify, request

import config

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "mendixdev": generate_password_hash(")cCR2_2J)v]\pJEU")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
        
        

os.environ['PATH'] = config.ENV_CONFIG['path']

handler = RotatingFileHandler(config.ENV_LOG['path'], maxBytes=1000000, backupCount=5)
handler.setLevel(logging.WARNING)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', None, "%"))
logger = logging.getLogger()
logger.addHandler(handler)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

tables = [
    'application_codes',
    'certificate_types',
    'coatings',
    'edge_types',
    'elements',
    'finishes',
    'grindings',
    'ingot_types',
    'icd_prs',
    'inspection_authority',
    'manufacturing_groups',
    'measure_types',
    'melting_codes',
    'product_types',
    'property_forms',
    'process_steps',
    'production_paths',
    'products',
    'process_routes',
    'process_route_details',
    'product_mark_instr',
    'organisation_units',
    'slab_types',
    'special_requirements',
    'standard_steel_types',
    'standards',
    'standard_tol_entries',
    'standard_tol_classes',
    'storing_locations',
    'surfaces',
    'test_method_param',
    'test_parameter_req',
    'transport_methods',
    'units_of_measure',
    'dual',
    'inner_coil_diameters', 
    'test_method_instr',
    'markings',
    'test_methods',
    'STANDARDTESTINSTR',
    'test_parameters'
    ]

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': str('wrong URL')})

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False
    
@app.route('/pf/<dbtable>', methods=['GET'])
@auth.login_required
def pf(dbtable):
    if dbtable not in tables:
        return jsonify({'error': 'table not allowed ' + dbtable})
    user = request.headers.get('user')
    if not user:
        return jsonify({'error': 'wrong user'})
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
        app.logger.warning(' GET ' + dbtable + ' ' + str(user) + ' ' + hostname + ' ' + ip)
        return jsonify({'data': items})
    except Exception as e:
       return jsonify({'error': str(e)})


@app.route('/sys2k/<dbtable>', methods=['GET'])
@auth.login_required
def sys2k(dbtable):
    user = request.headers.get('user')
    if not user:
        return jsonify({'error': 'wrong user'})
    connection = None
    try:
        connection = cx_Oracle.connect(config.DATABASE_CONFIG_SYS2K['user'],
                                       config.DATABASE_CONFIG_SYS2K['password'],
                                       config.DATABASE_CONFIG_SYS2K['host'])
        cur = connection.cursor()
         
        if dbtable == 'akid':
            result = cur.execute(f"""SELECT DISTINCT CUT_BURR_INSTR, EMB, PLASTN, PROD_MARK_FILM, QUALITY_INDICATOR, STOCK_INDICATOR FROM akid""")
        if dbtable == 'aordrad':
            result = cur.execute(f"""SELECT DISTINCT PRODMARKIN from AORDRAD""") 
        if dbtable == 'aordres':
            result = cur.execute(f"""SELECT DISTINCT id from AORDRES""")
        if dbtable == 'atvidorder':    
            result = cur.execute(f"""SELECT DISTINCT LANDKOD FROM ATVIDORDER""")
        if dbtable == 'bopsteg': 
            result = cur.execute(f"""SELECT DISTINCT PROCSTEG FROM BOPSTEG""")
        if dbtable == 'bpid': 
            result = cur.execute(f"""SELECT DISTINCT PRODTYP, KANT, LEVFORM, SPECKRAV, YTA FROM BPID""")
        if dbtable == 'dual':   
            result = cur.execute(f"""SELECT * FROM {dbtable}""")
            
        items = [dict(zip([key[0] for key in cur.description], row)) for row in result]
        cur.close()
        connection.close()
        app.logger.warning(' GET ' + dbtable + ' ' + str(user) + ' ' + hostname + ' ' + ip)
        return jsonify({'data': items})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
