#! /usr/bin/env python
from flask import Flask, render_template, url_for, request, json, jsonify
import numpy as np
import datetime

app = Flask(__name__)

# Config options - Make sure you 'config.py' file is created.
#app.config.from_object('config')

from .utils import *

@app.route('/question/',methods=['POST'])
def get_quest():
    """"""
    input_json = request.data.decode()
    input = json.loads(input_json)
    
    question = input['question']
    print("Question received: {}".format(question))
    
    predicted_tags = final_tag_set(question)
    
    return jsonify({'tags' : predicted_tags})


#curl -i -H "Content-Type: application/json" -X POST -d '{"question":"This is a test for Python <strong&>Flask API</strong> development where <code> toto </code>."}' http://frssldev01:5000/question/