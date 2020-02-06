#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import logging
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

#curl -X GET -i -H "Content-Type: application/json" -d "{\"id\":1}" http://127.0.0.1:8080/employees
@app.route('/employees', methods=['GET'])
def view_employee():
    print('%s') % (str(request.json['id']))
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))