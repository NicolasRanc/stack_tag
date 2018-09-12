#! /usr/bin/env python
from stack_tag import app

if __name__ == "__main__":
    app.run(debug=True)
    
    try:
        nltk.download('wordnet')
        nltk.download('stopword')
    except:
        print('nltk files already installed')
    
#Command lines to launch on FRSSLDEV01 server
#export FLASK_APP=~/app/dev/stack_tag/run.py
#export FLASK_DEBUG=1

#Launch application
#flask run --host=frssldev01

#Test of FRSSLDEV01
#curl -i -H "Content-Type: application/json" -X POST -d '{"question":"This is a test for Python <strong&>Flask API</strong> development where <code> toto </code>."}' http://frssldev01:5000/question/