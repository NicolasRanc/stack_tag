#! /usr/bin/env python
from flask import Flask, render_template, url_for, request, json, jsonify
import numpy as np
import datetime

app = Flask(__name__)

from .utils import *

@app.route('/question/',methods=['POST'])
def get_quest():
    """Returns json from HTML POST request. Input is json {'question': paragraph to be tagged}
    """
    input_json = request.data.decode()
    input = json.loads(input_json)
    
    question = input['question']
    print("Question received: {}".format(question))
    
    predicted_tags = final_tag_set(question)
    
    return jsonify({'tags' : predicted_tags})
