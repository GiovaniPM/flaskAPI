#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime, timedelta
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import hashlib
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

def conv115(codigo):

    linha = codigo['linha']

    dados = {}

    dados['CNPJ tomador'] = linha[0  :14 ]
    dados['Data Emissao'] = linha[81 :89 ]
    dados['Número NF   '] = linha[94 :103]
    dados['Valor NF    '] = linha[135:147]
    dados['Base ICMS   '] = linha[147:159]
    dados['Valor ICMS  '] = linha[159:171]
    dados['CNPJ emissor'] = codigo['cnpj_emissor']

    mensagem = dados['CNPJ tomador'] +\
               dados['Número NF   '] +\
               dados['Valor NF    '] +\
               dados['Base ICMS   '] +\
               dados['Valor ICMS  '] +\
               dados['Data Emissao'] +\
               dados['CNPJ emissor']

    dados['linha       '] = mensagem
    dados['hash antiga '] = linha[103:135]
    dados['hash nova   '] = hashlib.md5(mensagem.encode()).hexdigest().upper()

    return dados

@app.route('/cb', methods=['GET'])
def decompoe():
    reg = {}

    if request.json == None:
        return jsonify( { 'error': 'No parameters found.' } )
    else:
        if 'conv115' in request.json:
            if 'conv115' in request.json:
                reg['conv115'] = conv115(request.json['conv115'])
            print(reg)
        else:
            return jsonify( { 'error': 'No keys valid found.' } )

    json_result = reg
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))