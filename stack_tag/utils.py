#! /usr/bin/env python
import pickle

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.svm import LinearSVC

from stack_tag.models import Question

#dummy function needed for tfidf-vectorizer method (return token as it is)
def dummy_fun(token):
    return token

#text ="This is a test for Python <strong>Flask API</strong> development where <code> toto </code>."
    
def final_tag_set(text):
    """"""
    
    #Load models from pickle serialized object
    with open("stack_tag/model/"+filename, 'rb') as save_file:
    with open("model/"+filename, 'rb') as save_file:
        pickler = pickle.Unpickler(save_file)
        stacktag_models = pickler.load()
            
    tfidf_mono_vectorizer = stacktag_models["tdidf_vectorizer"]
    nmf_mod = stacktag_models["nmf_model"]
    linsvc_mod = stacktag_models["linearsvc_model"]
    tfidf_dict = tfidf_mono_vectorizer.get_feature_names()
    
    #Tokenize, remove stopword and lemmatize text (--> Bag-of-word)
    token = np.array([trokenize_text(text)])
    
    #transform bag-of-word in tf-idf vector
    tfidf_question = tfidf_mono_vectorizer.transform(token)
    
    #Predict principal tag from LinearSVC model
    principal_tag = linsvc_mod.predict(tfidf_question).tolist()
    
    #Predict secondary tag with NMF
    nmf_tags = tags_from_nmf(tfidf_question, tfidf_dict, nmf_mod, min_freq=0.01, max_words=4)
    
    #We remove from secondary tag if tag 
    secondary_tags = [tg for tg in nmf_tags if tg not in principal_tag]
    
    #Associate tags together
    return {'principal_tag': principal_tag,
            'secondary_tags': secondary_tags}


def trokenize_text(text):
    """"""
    text_2_modify = Question(text)
    text_2_modify.rm_code()
    text_2_modify.html_tag_rm()
    return text_2_modify.tokenize()


def tags_from_nmf(tfidf_question, tfidf_dict, nmf_mod, min_freq=0.01, max_words=4):
    """"""
    
    #model nmf from tfidf vector to compute W matrix
    w_matrix = nmf_mod.transform(tfidf_question)
    
    if w_matrix.max() >= min_freq:
        max_component = w_matrix.argmax()#Extract NMF max component index
        topic = nmf_mod.components_[max_component]#Extract corresponing maximum topic
        #Extract top 5 words associated to topics
        tags = [str(tfidf_dict[max_component]) for max_component in topic.argsort()[:-max_words - 1:-1]]
    
    else:
        tags=[]
        
    return tags


def tags_from_linearsvc(tfidf_question, linsvc_mod):
    """"""
    
    #Model nmf from tfidf vector
    predict_tag = linsvc_mod.predict(tfidf_question)
        
    return predict_tag