#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import logging
import os
import datetime
import json
import re

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

#Transformando um string em JSON
#import json 
#str = '{"from": {"id": "8", "name": "Mary Pinter"}, "message": "How ARE you?", "comments": {"count": 0}, "updated_time": "2012-05-01", "created_time": "2012-05-01", "to": {"data": [{"id": "1543", "name": "Honey Pinter"}]}, "type": "status", "id": "id_7"}'
#data = json.loads(str)
#post_id = data['id']
#post_type = data['type']
#print(post_id)
#print(post_type)

def isCpfValid(cpf):
    """ If cpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(cpf,str):
        return False
    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cpf)
    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False
    sum = 0
    weight = 10
    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum = sum + int(cpf[n]) * weight
        # Decrement weight
        weight = weight - 1
    verifyingDigit = 11 -  sum % 11
    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit
    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight
        # Decrement weight
        weight = weight - 1
    verifyingDigit = 11 -  sum % 11
    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit
    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

def isCnpjValid(cnpj):
    """ If cnpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(cnpj,str):
        return False
    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cnpj)
    # Checks if string has 11 characters
    if len(cpf) != 14:
        return False
    sum = 0
    weight = [5,4,3,2,9,8,7,6,5,4,3,2]
    """ Calculating the first cpf check digit. """
    for n in range(12):
        value =  int(cpf[n]) * weight[n]
        sum = sum + value
    verifyingDigit = sum % 11
    if verifyingDigit < 2 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = 11 - verifyingDigit
    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    for n in range(13):
        sum = sum + int(cpf[n]) * weight[n]
    verifyingDigit = sum % 11
    if verifyingDigit < 2 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = 11 - verifyingDigit
    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

#curl -X GET -i -H "Content-Type: application/json" -d "{\"id\":32,\"nome\":\"Lucas\",\"ano\":2020}" http://127.0.0.1:8080/employees
@app.route('/employees', methods=['GET'])
def view_employee():
    objects_list = []
    if request.json == None:
        abort(404)
    else:
        reg        = {}
        reg['01' ] = request.json['id']
        reg['02' ] = request.json['nome']
        reg['03' ] = str(datetime.datetime.now())
        if request.json['ano'] == 2020:
            reg['04' ] = 'Este ano'
        else:
            reg['04' ] = 'Outro ano'
        objects_list.append(reg)
        json_result = json.dumps(objects_list)
        return jsonify(json_result)

@app.route('/dv', methods=['GET'])
def view_cic():
    """ Service to validate CIC (CPF/CNPJ).

    Parameter: cic:string
    Return: True/False

    Uso:
        curl -X GET -i -H "Content-Type: application/json" -d "{\"cpf\":\"62256092020\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"cnpj\":\"30917504000131\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"cnpj\":\"30917504000131\", \"cpf\":\"62256092020\"}" http://127.0.0.1:8080/dv
    """
    reg          = {}
    if request.json == None:
        abort(404)
    if 'cnpj' in request.json:
        if not isinstance(request.json['cnpj'],str):
            abort(415)
        elif len(request.json['cnpj']) == 14:
            reg['cnpj' ] = isCnpjValid(request.json['cnpj'])
        else:
            abort(406)
    if 'cpf' in request.json:
        if not isinstance(request.json['cpf'],str):
            abort(415)
        elif len(request.json['cpf']) == 11:
            reg['cpf' ] = isCpfValid(request.json['cpf'])
        else:
            abort(406)
    json_result = json.dumps(reg)
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))