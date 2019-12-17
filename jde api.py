#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from json import dumps
from requests import post

import logging
import cx_Oracle
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

@auth.verify_password
def verify_password(username, password):
    api_url = 'http://api.corp-app-hlg.rbs.com.br/ad/user'
    group_list = ["G-INT-Colaboradores"]
    headers = {'Content-type': 'application/json'}
    data_dict_to_be_send = {
                "login": username,
                "password": password,
                "adgroup": group_list,
                "application": "PortalApis"}
    data_json_format = dumps(data_dict_to_be_send, ensure_ascii=False)
    r = post(api_url, data=data_json_format, headers=headers)
    output_req = "%s" % r
    if output_req != '<Response [200]>':
        return False
    else:
        return True

@auth.error_handler
def unauthorized():
    return jsonify( { 'error': 'Unauthorized access' } )

def createConnection():
    try:
        db_host = os.environ['DB_HOST']
    except Exception:
        db_host = 'ora12cdev-scan.rbs.com.br'
    try:
        db_port = int(os.environ['DB_PORT'])
    except Exception:
        db_port = 1544
    try:
        db_servicename = os.environ['DB_SERVICENAME']
    except Exception:
        db_servicename = 'jdehlg.rbs.com.br'
    try:
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
    except Exception:
        db_user = 'USER_JDE_QUERY'
        db_pass = 'djangov1v3'
    conn_string = "\
                   (DESCRIPTION =\
                        (ADDRESS_LIST =\
                            (ADDRESS = (PROTOCOL = TCP)\
                                (HOST = %s)\
                                (PORT = %s))\
                            )\
                        (CONNECT_DATA =\
                            (SERVICE_NAME = %s)\
                        )\
                    )" % (db_host, str(db_port), db_servicename)
    return cx_Oracle.connect(user=db_user, password=db_pass, dsn=conn_string, encoding='UTF-8')

@app.route('/')
def index():
    return 'The application is running!'

@app.route('/cic/<tax>', methods=['GET'])
@auth.login_required
def get_cic(tax):
    conn = createConnection()
    cur = conn.cursor()
    sql_string = '''SELECT\
                        ABAN8,\
                        ABAT1,\
                        ABALKY,\
                        ABALPH,\
                        ALADD1,\
                        ALADD2,\
                        ALADDZ,\
                        ALCTY1,\
                        ALADDS,\
                        ALCTR\
                    FROM\
                        PRODDTAXE.F0101\
                    INNER JOIN PRODDTAXE.F0116\
                        ON ALAN8 = ABAN8\
                    WHERE\
                        ABTAX = '%s' ''' % (tax)
    cur.execute(sql_string)
    rv = cur.fetchall()    
    if rv is None:
        abort(204)
    cur.close()
    conn.close()
    return jsonify(rv)	

@app.route('/oc/<cia>/<int:ordem>/<tipo>', methods=['GET'])
@auth.login_required
def get_oc(cia, ordem, tipo):
    conn = createConnection()
    cur = conn.cursor()
    sql_string = '''SELECT\
                        PDLNID/1000,\
                        PDLITM,\
                        PDUOM,\
                        PDUORG,\
                        PDAEXP/100\
                    FROM\
                        PRODDTAXE.F4311\
                    WHERE\
                        PDKCOO = '%s' AND\
                        PDDOCO = %s AND\
                        PDDCTO = '%s' ''' % (cia, ordem, tipo)
    cur.execute(sql_string)
    rv = cur.fetchall()
    if rv is None:
        abort(204)
    cur.close()
    conn.close()
    return jsonify(rv)	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))