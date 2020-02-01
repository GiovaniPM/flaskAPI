from flask import Flask, jsonify
from threading import Thread
#from flask_restful import Resource, Api
import json
import random

app = Flask('')
api = Api(app)

@app.route('/')
def home():
  return "I'm alive"

#################
##APi using Flask
###################
@app.route('/testing', methods=['GET'])
def testing():
  return jsonify({"Test" : "Successful"})  

@app.route('/api/add/<int:num>', methods=['GET'])
def add(num):
  return jsonify({f"{num} + {num}" : num + num})

@app.route('/api/name/<string:name>', methods=['GET'])
def get_name(name):
  return jsonify({"Your name": name})

#################################
##API USING FLASK-RESTFUL

class Test(Resource):
  def get(self):
    return jsonify({"Type": "flask-restful"})

def get_quotes(quote_type):
  if quote_type == "motivation":
    file_address = 'Quotes/motivation.json'
  elif quote_type == "funny":
    file_address = 'Quotes/funny.json'
  else:
    file_address = 'errormsg.json'  
  with open(file_address, 'r') as quotefile:
    data = json.load(quotefile)
  quote = random.choice(list(data['Quotes']))
  return quote

def get_facts(fact_type):
  if fact_type == "random":
    file_address = 'Facts/random.json'
  elif fact_type == "technology":
    file_address = 'Facts/technology.json'
  else:
    file_address = 'errormsg.json'  
  with open(file_address, 'r') as factfile:
    data = json.load(factfile)
  fact = random.choice(list(data['Facts']))
  return fact  

class Quotes(Resource):
  def get(self, quote_type):
    return get_quotes(quote_type)

class Facts(Resource):
  def get(self, fact_type):
    return get_facts(fact_type)

api.add_resource(Test, '/api/restful')
api.add_resource(Quotes, '/api/quotes/<string:quote_type>')
api.add_resource(Facts, '/api/facts/<string:fact_type>')

#http://127.0.0.1:7210/api/facts/random
#http://127.0.0.1:7210/api/facts/technology
#http://127.0.0.1:7210/api/quotes/motivation
#http://127.0.0.1:7210/api/quotes/funny
#http://127.0.0.1:7210/api/restful

def run():
  app.run(host='0.0.0.0',port=7210)
  
t = Thread(target=run)
t.start()