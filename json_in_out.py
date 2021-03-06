#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import datetime
import json
import logging
import math
import os
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))