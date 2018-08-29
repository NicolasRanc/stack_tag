#! /usr/bin/env python
from flask import Flask, render_template, url_for, request, json, jsonify
import numpy as np
import datetime

app = Flask(__name__)

# Config options - Make sure you 'config.py' file is created.
#app.config.from_object('config')

from .utils import *

@app.route('/prediction/<str:quest',methods=['GET'])
def get_quest(quest):
    """"""
    print("Question received: {}".format(quest))
    
    predicted_tags = final_tag_set(quest)
    
    return jsonify({'Tags' : predicted_tags})