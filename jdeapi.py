#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from requests import post
from json import dumps
from unicodedata import normalize

import collections
import logging
import cx_Oracle
import os
import datetime
import json

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})
loginid = ''

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

def outputlog(text): # TODO: Ativar modo debug
    text = str(text)
    print(loginid," ".join(text.split()))

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

@auth.verify_password
def verify_password(username, password):
    global loginid
    loginid = username + ' ' + str(datetime.datetime.now().timestamp())
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

@app.route('/')
def index():
    return 'The application is running!'

@app.route('/help')
def help():
    outputhelp = "Services on this server:\n<br/>\
  cic          usage: curl -u <network user>:<password> -X GET -i http://127.0.0.1:8080/cic/cic number\n<br/>\
  oc           usage: curl -u <network user>:<password> -X GET -i http://127.0.0.1:8080/oc/cia/oc/type\n<br/>\
  menu         usage: curl -u <network user>:<password> -X GET -i http://127.0.0.1:8080/menu/appube"
    return outputhelp

"""
 ██████╗██╗ ██████╗
██╔════╝██║██╔════╝
██║     ██║██║
██║     ██║██║
╚██████╗██║╚██████╗
 ╚═════╝╚═╝ ╚═════╝
Retorna os endereços de um CIC
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/cic/82951328000158
"""

@app.route('/cic/<tax>', methods=['GET'])
@auth.login_required
def get_cic(tax):
    par = '/cic/' + str(tax)
    outputlog(datetime.datetime.now())
    conn = createConnection()
    cur = conn.cursor()
    sql_string =   "SELECT\
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
                        ABTAX = rpad(:tax,20,' ')" # Quando usar bind, deve observar espaços em branco
    cur.prepare(sql_string)
    cur.execute(None, {'tax': tax})
    rv = cur.fetchall()    
    outputlog(par.replace(' ', '')) 
    outputlog(sql_string)
    outputlog(datetime.datetime.now())
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        for row in rv:
            reg                = {}
            reg['Codigo' ]     = row[0]
            reg['Tipo' ]       = remover_acentos(row[1])
            reg['Alternativo'] = remover_acentos(row[2])
            reg['Nome' ]       = remover_acentos(row[3])
            reg['Endereco1' ]  = remover_acentos(row[4])
            reg['Endereco2' ]  = remover_acentos(row[5])
            reg['CEP' ]        = remover_acentos(row[6])
            reg['Cidade' ]     = remover_acentos(row[7])
            reg['Estado' ]     = remover_acentos(row[8])
            reg['Pais' ]       = remover_acentos(row[9])
            objects_list.append(reg)
        json_result = json.dumps(objects_list)
        cur.close()
        conn.close()
    return jsonify(json_result)

"""
 ██████╗  ██████╗
██╔═══██╗██╔════╝
██║   ██║██║
██║   ██║██║
╚██████╔╝╚██████╗
 ╚═════╝  ╚═════╝
Retorna linhas de uma OC
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/oc/00610/2819/OM
"""

@app.route('/oc/<cia>/<int:ordem>/<tipo>', methods=['GET'])
@auth.login_required
def get_oc(cia, ordem, tipo):
    par = '/oc/' + cia + '/' + str(ordem) + '/' + tipo
    outputlog(datetime.datetime.now())
    conn = createConnection()
    cur = conn.cursor()
    sql_string =   "SELECT\
                        PDLNID/1000,\
                        TRIM(PDLITM),\
                        TRIM(PDDSC1),\
                        TRIM(PDDSC2),\
                        PDUOM,\
                        PDUORG,\
                        PDAEXP/100,\
                        TRIM(PDANI)\
                    FROM\
                        PRODDTAXE.F4311\
                    WHERE\
                        PDKCOO = :cia AND\
                        PDDOCO = :ordem AND\
                        PDDCTO = :tipo "
    cur.prepare(sql_string)
    cur.execute(None, {'cia': cia, 'ordem': ordem, 'tipo': tipo})
    rv = cur.fetchall()
    outputlog(par.replace(' ', ''))
    outputlog(sql_string)
    outputlog(datetime.datetime.now())
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        for row in rv:
            reg               = {}
            reg['Linha' ]     = row[0]
            reg['Item' ]      = remover_acentos(row[1])
            reg['Descricao1'] = remover_acentos(row[2])
            reg['Descricao2'] = remover_acentos(row[3])
            reg['UM' ]        = remover_acentos(row[4])
            reg['Quantidade'] = row[5]
            reg['Valor' ]     = row[6]
            reg['Conta' ]     = remover_acentos(row[7])
            objects_list.append(reg)
        json_result = json.dumps(objects_list)
        cur.close()
        conn.close()
    return jsonify(json_result)

"""
███╗   ███╗███████╗███╗   ██╗██╗   ██╗
████╗ ████║██╔════╝████╗  ██║██║   ██║
██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝
Retorna o caminho de menu de um app/ube
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/menu/P4310
"""

@app.route('/menu/<app>', methods=['GET'])
@auth.login_required
def get_menu(app):
    par = '/menu/' + app
    outputlog(datetime.datetime.now())
    conn = createConnection()
    cur = conn.cursor()
    sql_string =   "SELECT\
                        tst.task,\
                        f9000.tmlngtask,\
                        f9000.tmobnm,\
                        f9000.tmver,\
                        f9000.tmfmnm\
                    FROM   (SELECT\
                                caminho,\
                                substr(CASE WHEN nivel = 1 THEN caminho ELSE replace(caminho, LAG(caminho) OVER(ORDER BY caminho)) END, 2) task,\
                                nivel\
                            FROM   (SELECT DISTINCT\
                                        sys_connect_by_path(task, '/') caminho,\
                                        level nivel\
                                    FROM   (SELECT\
                                                f9001.trchildtsk pai,\
                                                f9001.trparnttsk filho,\
                                                TRIM(f9000.tmtasknm) task,\
                                                TRIM(f9000.tmobnm) obj\
                                            FROM\
                                                prodctlxe.f9000 f9000\
                                                INNER JOIN prodctlxe.f9001 f9001 ON f9001.trchildtsk = f9000.tmtaskid\
                                            WHERE\
                                                f9000.tmtasknm LIKE 'RBS%%')\
                                    CONNECT BY NOCYCLE\
                                        PRIOR filho = pai\
                                    START WITH obj = UPPER(TRIM(:app)))\
                            ORDER BY\
                                caminho) tst\
                    INNER JOIN prodctlxe.f9000 f9000 ON TRIM(f9000.tmtasknm) = tst.task\
                    ORDER BY\
                        caminho DESC"
    cur.prepare(sql_string)
    cur.execute(None, {'app': app})
    rv = cur.fetchall()
    outputlog(par.replace(' ', ''))
    outputlog(sql_string)
    outputlog(datetime.datetime.now())
    if rv is None:
        cur.close()
        conn.close()
        abort(204)
    else:
        objects_list = []
        for row in rv:
            reg              = {}
            reg['Task' ]     = remover_acentos(row[0])
            reg['Descricao'] = remover_acentos(row[1])
            reg['App' ]      = remover_acentos(row[2])
            reg['Versao' ]   = remover_acentos(row[3])
            reg['Tela' ]     = remover_acentos(row[4])
            objects_list.append(reg)
        json_result = json.dumps(objects_list)
        cur.close()
        conn.close()
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))