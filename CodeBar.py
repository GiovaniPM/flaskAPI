#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime, timedelta
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import datetime
import time
import json
import logging
import math
import os
import re

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

def ipte(codigo):
    dados = {}
    codigo = codigo.replace(" ", "").replace(".", "")
    data_base = datetime.datetime(1997, 10, 7)
    
    dados['banco'        ] =     codigo[0 :3 ]
    dados['moeda'        ] =     codigo[3 :4 ]
    dados['carteira'     ] =     codigo[4 :7 ]
    dados['nosso numero' ] =     codigo[7 :9 ] + codigo[10:16]
    dados['dac1'         ] =     codigo[9 :10]
    dados['dac2'         ] =     codigo[16:17]
    dados['agencia'      ] =     codigo[17:20] + codigo[21:22]
    dados['dac3'         ] =     codigo[20:21]
    dados['conta'        ] =     codigo[22:28]
    dados['zero'         ] =     codigo[28:31]
    dados['dac4'         ] =     codigo[31:32]
    dados['dac5'         ] =     codigo[32:33]
    dados['fator'        ] =     codigo[33:37]
    dados['valor'        ] = int(codigo[37:47])/100
    dados['vencimento'] = data_base + datetime.timedelta(days=int(dados['fator']))
    
    return dados
         
@app.route('/cb', methods=['GET'])
def view_dv():
    reg = {}
    
    if request.json == None:
        return jsonify( { 'error': 'No parameters found.' } )
    elif 'ipte' in request.json:
        reg['ipte'] = ipte(request.json['ipte'])
    else:
        return jsonify( { 'error': 'No keys valid found.' } )
    
    json_result = reg
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))