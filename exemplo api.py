#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import logging
import cx_Oracle
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

@auth.get_password
def get_password(username):
    #print(generate_password_hash('python'))
    if username == 'miguel':
        return 'python'
    if username == 'giovanipm':
        return 'loco'
    return None

@auth.error_handler
def unauthorized():
    return jsonify( { 'error': 'Unauthorized access' } )

def creatConnection():
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
        db_user = 'GIOVANI_MESQUITA'
        db_pass = 'ScQz#waAM5'
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

# def creatConnection():
#     # Read MySQL Environment Parameters
#     connectString = os.environ.get('MYSQLCS_CONNECT_STRING', 'localhost:3306/myDB') 
#     hostname = connectString[:connectString.index(":")]
#     database = connectString[connectString.index("/")+1:]
#     conn = pymysql.connect(host=hostname, 
# 	                       port=int(os.environ.get('MYSQLCS_MYSQL_PORT', '3306')), 
# 						   user=os.environ.get('MYSQLCS_USER_NAME', 'root'), 
# 						   passwd=os.environ.get('MYSQLCS_USER_PASSWORD', ''), 
# 						   db=database,
# 						   cursorclass=pymysql.cursors.DictCursor)
#     return conn;

@app.route('/')
def index():
    return 'The application is running!'
	
@app.route('/employees/setupdb')
def setupDB():
    conn = creatConnection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE EMPLOYEE (
				  ID INTEGER NOT NULL,
				  FIRSTNAME VARCHAR(255),
				  LASTNAME VARCHAR(255),
				  EMAIL VARCHAR(255),
				  PHONE VARCHAR(255),
				  BIRTHDATE VARCHAR(10),
				  TITLE VARCHAR(255),
				  DEPARTMENT VARCHAR(255),
				  PRIMARY KEY (ID)
				  ) ''') 
    conn.commit()
    cur.close()
    conn.close()
    return 'The EMPLOYEE tables was created succesfully'
	
@app.route('/employees')
def employees():
    conn = creatConnection()
    cur = conn.cursor()
    cur.execute('''SELECT ID, FIRSTNAME, LASTNAME, EMAIL, PHONE, BIRTHDATE, TITLE, DEPARTMENT FROM EMPLOYEE''')
    results = cur.fetchall()	
    cur.close()
    conn.close()
    return jsonify(results)	

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    conn = creatConnection()
    cur = conn.cursor()
    cur.execute('''SELECT ID, FIRSTNAME, LASTNAME, EMAIL, PHONE, BIRTHDATE, TITLE, DEPARTMENT FROM EMPLOYEE WHERE ID = %s'''%(employee_id))
    rv = cur.fetchone()    
    if rv is None:
        abort(404)
    cur.close()
    conn.close()
    return jsonify(rv)	

@app.route('/cic/<int:tax>', methods=['GET'])
@auth.login_required
def get_cic(tax):
    conn = creatConnection()
    cur = conn.cursor()
    cur.execute('''SELECT ABAN8, ABAT1, ABALKY, ABALPH FROM PRODDTAXE.F0101 WHERE ABTAX = '%s' '''%(tax))
    rv = cur.fetchall()    
    if rv is None:
        abort(404)
    cur.close()
    conn.close()
    return jsonify(rv)	

@app.route('/employees', methods=['POST'])
def create_employee():
    conn = creatConnection()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO EMPLOYEE (ID, FIRSTNAME, LASTNAME, EMAIL, PHONE, BIRTHDATE, TITLE, DEPARTMENT) 
	                VALUES('%s','%s','%s','%s','%s','%s','%s','%s') '''%(request.json['id'],request.json['firstName'],request.json['lastName'],
				    request.json['email'],request.json['phone'],request.json['birthDate'],request.json['title'],request.json['dept']))    
        conn.commit()
        message = {'status': 'New employee record is created succesfully'}
        cur.close()	 
    except Exception as e:
        logging.error('DB exception: %s' % e)
        message = {'status': 'The creation of the new employee failed.'}
    conn.close()
    return jsonify(message)

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    conn = creatConnection()
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE EMPLOYEE SET FIRSTNAME='%s', LASTNAME='%s', EMAIL='%s', PHONE='%s', BIRTHDATE='%s', TITLE='%s', DEPARTMENT='%s' 
	               WHERE ID=%s '''%(request.json['firstName'],request.json['lastName'],
				   request.json['email'],request.json['phone'],request.json['birthDate'],request.json['title'],request.json['dept'],employee_id))    
        conn.commit()
        message = {'status': 'The employee record is updated succesfully'}
        cur.close()	 
    except Exception as e:
        logging.error('DB exception: %s' % e)	
        message = {'status': 'Employee update failed.'}
    conn.close()
    return jsonify(message)

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    conn = creatConnection()
    cur = conn.cursor()
    try:
        cur.execute('''DELETE FROM EMPLOYEE WHERE ID=%s '''%(employee_id))    
        message = {'status': 'The employee record is deleted succesfully'}
        conn.commit()
        cur.close()	 
    except Exception as e:
        logging.error('DB exception: %s' % e)	
        message = {'status': 'Employee delete failed.'}
    conn.close()
    return jsonify(message)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))