#!/usr/bin/env python
from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": "POST,DELETE,PUT,GET,OPTIONS"}})

def conv115(codigo):
    linha = codigo['linha']

    dados = {
        'CNPJ tomador': linha[0:14],
        'Data Emissao': linha[81:89],
        'Número NF': linha[94:103],
        'Valor NF': linha[135:147],
        'Base ICMS': linha[147:159],
        'Valor ICMS': linha[159:171],
        'CNPJ emissor': codigo['cnpj_emissor']
    }

    mensagem = ''.join([
        dados['CNPJ tomador'],
        dados['Número NF'],
        dados['Valor NF'],
        dados['Base ICMS'],
        dados['Valor ICMS'],
        dados['Data Emissao'],
        dados['CNPJ emissor']
    ])

    dados.update({
        'linha': mensagem,
        'hash antiga': linha[103:135],
        'hash nova': hashlib.md5(mensagem.encode()).hexdigest().upper()
    })

    return dados

@app.route('/cb', methods=['GET'])
def decompoe():
    if not request.json or 'conv115' not in request.json:
        return jsonify({'error': 'No parameters or keys valid found.'})

    reg = {'result': conv115(request.json['conv115'])}
    return jsonify(reg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8080')))
