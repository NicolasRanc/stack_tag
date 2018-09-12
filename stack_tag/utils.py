#! /usr/bin/env python
import pickle
import os

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.svm import LinearSVC

from stack_tag.models import Question
	
def final_tag_set(text):
    """Returns tags predicted from paragraph. Uses NMF un-supervised and SGDC supervised model trained
    on cleaned Stackoverflow question and tags.
    Args:
        text: text paragraph."""

    #Load models from pickle serialized object
    filename = "stack_tag_models"
    print(os.getcwd())
    with open("stack_tag/model/"+filename, 'rb') as save_file:
        pickler = pickle.Unpickler(save_file)
        stacktag_models = pickler.load()#problem on dummy_fun associated to vecorizer. Look if possible to set-up parameter for not accounting anymore on own function.

    tfidf_vectorizer = stacktag_models["tdidf_vectorizer"]
    nmf_model = stacktag_models["nmf_model"]
    sgdc_model = stacktag_models["sgdc_model"]

    tfidf_dict = tfidf_vectorizer.get_feature_names()
    
    #Tokenize, remove stopword and lemmatize text (--> Bag-of-word)
    token = np.array([trokenize_text(text)])
    
    #transform bag-of-word in tf-idf vector
    tfidf_question = tfidf_vectorizer.transform(token)
    
    #Predict principal tag from LinearSVC model
    principal_tag = sgdc_model.predict(tfidf_question)[0]
    
    #Predict secondary tag with NMF
    nmf_tags = top_tags_from_nmf(token, tfidf_vectorizer, nmf_model, score_min=0.12)
    
    #We remove from secondary tag if tag
    secondary_tags = {k:v for k,v in nmf_tags.items() if k != principal_tag}
    
    #Associate tags together
    return {'principal_tag': principal_tag,
            'secondary_tags': secondary_tags}


def trokenize_text(text):
    """Returns tokenized text (stopword removed and lemmatization of words and verb).
    Args:
        text: text paragraph to tokenize."""
    text_2_modify = Question(text)
    text_2_modify.rm_code()
    text_2_modify.html_tag_rm()
    return text_2_modify.tokenize()


def top_tags_from_nmf(x, vec_model, nmf_mod, score_min=0.05):
    """Returns dictionnary with words maximally associated to document and their relative NMF score.
    Score of words are calculated by multiplication between NMF transformed W matrix and NMF fitted H
    (vocabulary) value to get importance of each words into topic definition.
    Args:
        x: Token to be analyzed (list of ngrams)
        vec_model: Vectorizer model used for TFIDF calculation
        nmf_mod: Trained NMF model
        score_min: threshold score for keeping word
    """
    tfidf_target = vec_model.transform(x)
    target_nmf_trans = nmf_mod.transform(tfidf_target)
    
    tags_scores = np.dot(target_nmf_trans, nmf_mod.components_).tolist()[0]

    dict_tags_score = dict(zip(vec_model.get_feature_names(), tags_scores))
    
    return { k: v for k, v in dict_tags_score.items() if v >= score_min }