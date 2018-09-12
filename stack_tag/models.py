#! /usr/bin/env python

import re

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from .views import app


class Question():
    '''Class Question contains methods tokenize'''

    def __init__(self, text):
        self.question = text
        self.token = []

    def html_tag_rm(self):
        """Returns new string without corresponding opening and closing html tag.
        Keeps the information within tags.
        Agrs:
            self: the text paragraph
        """
        
        #create set of html tags
        html_tag_set = set()
        tag_set = set(re.findall(r"</.*?>", self.question))
        cleaned_tag_set = {x.replace('</', '').replace('>', '').lower() for x in tag_set}
        html_tag_set |= cleaned_tag_set

        #Remove opening and closing html tags
        for tag in html_tag_set:
            list_of_tag_forms = [tag.lower(), tag.upper(), tag.capitalize()]

            for tag_script in list_of_tag_forms:
                oppen_tag_reg = "<" + tag_script + ".*?>"
                close_tag_reg =  "</" + tag_script + ".*?>"
                self.question = re.sub(r'|'.join((oppen_tag_reg, close_tag_reg)), '', self.question)

        return self.question


    def rm_code(self):
        """Returns new paragraph without anything within html code tag.
        Args:
            self: the text paragraph
        """
        tag = "code"
        list_of_tag_forms = [tag.lower(), tag.upper(), tag.capitalize()]

        #cleaned_seq = self.question
        for tag_script in list_of_tag_forms:    
            oppen_tag = r"<"+tag_script+".*?>"
            close_tag = r"</"+tag_script+".*?>"
            my_regex = re.compile(r""+oppen_tag+"(.*?)"+close_tag, re.S|re.M)
            self.question = re.sub(my_regex, '', self.question)
            #cleaned_seq = re.sub(my_regex, '', cleaned_seq)

        return self.question


    def tokenize(self):
        """Returns tokenized list with stopword removed and lemmatized words.
        nltk module is basic for text transformation.
        Args:
            self: the text paragraph
        """
        tokenizer = nltk.RegexpTokenizer(r'[\w\+\-\#\\*]+')
        lmtzr = WordNetLemmatizer()

        sw = set(tuple(nltk.corpus.stopwords.words('english')))

        tokens = tokenizer.tokenize(self.question.lower())

        stpwd_cleaned_token = [w for w in tokens if not w in list(sw)]

        lem_word_list = [lmtzr.lemmatize(i) for i in stpwd_cleaned_token]#lemmatize all nouns
        self.token = [lmtzr.lemmatize(j,'v') for j in lem_word_list]#lemmatize verbs

        return self.token