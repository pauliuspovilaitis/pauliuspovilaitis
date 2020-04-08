#!/usr/bin/python

import logging
import os
import socket
from logging.handlers import RotatingFileHandler

import cx_Oracle
from flask import Flask, jsonify, request

import config

app = Flask(__name__)
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
    'slab_types',
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
    'test_method_instr',
    'test_method_param',
    'test_methods',
    'test_parameter_req',
    'test_parameters',
    'transport_methods',
    'units_of_measure',
    'dual']


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': str('wrong URL')})


@app.route('/pf/<dbtable>', methods=['GET'])
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
def sys2k(dbtable):
    if dbtable not in tables:
        return jsonify({'error': 'table not allowed'})
    user = request.headers.get('user')
    if not user:
        return jsonify({'error': 'wrong user'})
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
        app.logger.warning(' GET ' + dbtable + ' ' + str(user) + ' ' + hostname + ' ' + ip)
        return jsonify({'data': items})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
