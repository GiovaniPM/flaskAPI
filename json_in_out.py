#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import math
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

def isEctValid(ect):
    """ If ect in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(ect,str):
        return False
    # Remove some unwanted characters
    ect = re.sub("[^0-9]",'',ect)
    # Checks if string has 9 characters
    if len(ect) != 9:
        return False
    sum = 0
    weight = [8,6,4,2,3,5,9,7]
    """ Calculating the ect check digit. """
    for n in range(8):
        sum = sum + int(ect[n]) * weight[n]
    verifyingDigit = 11 -  sum % 11
    if verifyingDigit == 0:
        firstVerifyingDigit = 5
    elif verifyingDigit == 1:
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit
    if ect[-1:] == "%s" % (firstVerifyingDigit):
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

def isCertidaoValid(certidao):
    """ If certidao in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(certidao,str):
        return False
    # Remove some unwanted characters
    certidao = re.sub("[^0-9]",'',certidao)
    # Checks if string has 11 characters
    if len(certidao) != 32:
        return False
    sum = 0
    weight = [2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9]
    """ Calculating the first certidao check digit. """
    for n in range(30):
        value =  int(certidao[n]) * weight[n]
        sum = sum + value
    firstVerifyingDigit = sum % 11
    if firstVerifyingDigit == 10:
        firstVerifyingDigit = 1
    """ Calculating the second check digit of certidao. """
    sum = 0
    weight = [1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9]
    for n in range(31):
        sum = sum + int(certidao[n]) * weight[n]
    secondVerifyingDigit = sum % 11
    if secondVerifyingDigit == 10:
        secondVerifyingDigit = 1
    if certidao[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

def isProcessoValid(processo):
    """ If processo in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(processo,str):
        return False
    # Remove some unwanted characters
    processo = re.sub("[^0-9]",'',processo)
    # Checks if string has 11 characters
    if len(processo) != 20:
        return False
    """ Calculating the processo check digit. """
    sum = int(processo[0:7]+processo[9:20])*100
    VerifyingDigit = 98 - (sum % 97)
    if int(processo[7:9]) == VerifyingDigit:
        return True
    return False

def isCreditoValid(credito):
    """ If credito in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(credito,str):
        return False
    # Remove some unwanted characters
    credito = re.sub("[^0-9]",'',credito)
    # Checks if string has 11 characters
    if len(credito) != 16:
        return False
    """ Calculating the credito check digit. """
    sum = 0
    weight = [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2]
    """ Calculating the first certidao check digit. """
    for n in range(15):
        value =  int(credito[n]) * weight[n]
        if value > 9:
            value = value - 9
        sum = sum + value
    VerifyingDigit = (math.ceil(sum/10)*10)-sum
    if int(credito[-1:]) == VerifyingDigit:
        return True
    return False

def isNfeValid(nfe):
    """ If nfe in the Brazilian format is valid, it returns True, otherwise, it returns False. """
    # Check if type is str
    if not isinstance(nfe,str):
        return False
    # Remove some unwanted characters
    nfe = re.sub("[^0-9]",'',nfe)
    # Checks if string has 11 characters
    if len(nfe) != 44:
        return False
    """ Calculating the nfe check digit. """
    sum = 0
    weight = [4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2]
    """ Calculating the first certidao check digit. """
    for n in range(43):
        value =  int(nfe[n]) * weight[n]
        sum = sum + value
    VerifyingDigit = 11 - (sum % 11)
    if int(nfe[-1:]) == VerifyingDigit:
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
def view_dv():
    """
    Description:
        Service to validate Digit Verification.
    Parameter:
        JSON {"certidao":string,
              "cnpj":string,
              "cpf":string
              "credito":string
              "ect":string
              "nfe":string
              "processo":string}
    Return:
        True/False per each parameter passed named
        JSON {"certidao":True/False,
              "cnpj":True/False,
              "cpf":True/False
              "credito":True/False
              "ect":True/False
              "nfe":True/False
              "processo":True/False}
    Usage:
        curl -X GET -i -H "Content-Type: application/json" -d "{\"certidao\":\"10453901552013100012021000012321\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"cnpj\":\"30917504000131\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"cpf\":\"62256092020\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"credito\":\"5491670040304243\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"ect\":\"473124829\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"nfe\":\"43171207364617000135550000000120141000120146\"}" http://127.0.0.1:8080/dv
        curl -X GET -i -H "Content-Type: application/json" -d "{\"processo\":\"00020802520125150049\"}" http://127.0.0.1:8080/dv

        curl -X GET -i -H "Content-Type: application/json" -d "{\"certidao\":\"10453901552013100012021000012321\",\"cnpj\":\"30917504000131\", \"cpf\":\"62256092020\",\"credito\":\"5491670040304243\",\"ect\":\"473124829\",\"nfe\":\"43171207364617000135550000000120141000120146\",\"processo\":\"00020802520125150049\"}" http://127.0.0.1:8080/dv
    Exemplo:
        $ curl -X GET -i -H "Content-Type: application/json" -d "{\"certidao\":\"10453901552013100012021000012321\",\"cnpj\":\"30917504000131\", \"cpf\":\"62256092020\",\"credito\":\"5491670040304243\",\"ect\":\"473124829\",\"nfe\":\"43171207364617000135550000000120141000120146\",\"processo\":\"00020802520125150049\"}" http://127.0.0.1:8080/dv
          % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
        100   349  100   123  100   226  61500   110k --:--:-- --:--:-- --:--:--  340k
        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 123
        Access-Control-Allow-Origin: *
        Server: Werkzeug/0.16.0 Python/3.8.1
        Date: Mon, 17 Feb 2020 18:48:18 GMT
        
        "{\"certidao\": true, \"cnpj\": true, \"cpf\": true, \"credito\": true, \"ect\": true, \"nfe\": true, \"processo\": true}"
    """
    # TODO: Make the validation routine
    # TODO: Make the accounting routine
    reg          = {}
    if request.json == None:
        abort(404)
    elif 'nfe' in request.json or 'credito' in request.json or 'processo' in request.json or 'certidao' in request.json or 'ect' in request.json or 'cnpj' in request.json or 'cpf' in request.json:
        if 'certidao' in request.json:
            if not isinstance(request.json['certidao'],str):
                abort(415)
            elif len(request.json['certidao']) == 32:
                reg['certidao' ] = isCertidaoValid(request.json['certidao'])
            else:
                abort(406)
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
        if 'credito' in request.json:
            if not isinstance(request.json['credito'],str):
                abort(415)
            elif len(request.json['credito']) == 16:
                reg['credito' ] = isCreditoValid(request.json['credito'])
            else:
                abort(406)
        if 'ect' in request.json:
            if not isinstance(request.json['ect'],str):
                abort(415)
            elif len(request.json['ect']) == 9:
                reg['ect' ] = isEctValid(request.json['ect'])
            else:
                abort(406)
        if 'nfe' in request.json:
            if not isinstance(request.json['nfe'],str):
                abort(415)
            elif len(request.json['nfe']) == 44:
                reg['nfe' ] = isNfeValid(request.json['nfe'])
            else:
                abort(406)
        if 'processo' in request.json:
            if not isinstance(request.json['processo'],str):
                abort(415)
            elif len(request.json['processo']) == 20:
                reg['processo' ] = isProcessoValid(request.json['processo'])
            else:
                abort(406)
        json_result = json.dumps(reg)
        return jsonify(json_result)
    else:
        abort(405)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))