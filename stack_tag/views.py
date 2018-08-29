#! /usr/bin/env python
from flask import Flask, render_template, url_for, request, json, jsonify
import numpy as np
import datetime

app = Flask(__name__)

# Config options - Make sure you 'config.py' file is created.
#app.config.from_object('config')

from .utils import *

@app.route('/question/<string:quest>',methods=['GET'])
def get_quest(quest):
    """"""
    print("Question received: {}".format(quest))
    
    predicted_tags = final_tag_set(quest)
    
    return jsonify({'Tags' : predicted_tags})


#curl -i http://frssldev01:5000/question/This%20is%20a%20test%20for%20Python%20&lt;strong&gt;Flask%20API&lt;/strong&gt;%20development%20where%20&lt;code&gt;%20toto%20&lt;/code&gt;.
#curl -i http://frssldev01:5000/question/This%20is%20a%20test%20for%20Python

#curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks