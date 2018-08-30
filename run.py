#! /usr/bin/env python
from stack_tag import app

import nltk
nltk.download('wordnet')
nltk.download('stopword')

if __name__ == "__main__":
    app.run(debug=True)
    
#Command lines to launch on FRSSLDEV01 server
#export FLASK_APP=~/app/dev/stack_tag/run.py
#export FLASK_DEBUG=1

#Launch application
#flask run --host=frssldev01