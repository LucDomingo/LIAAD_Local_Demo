from lxml import html
from lxml.html.clean import clean_html

import urllib.request
import json    

import nltk
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize

from nltk.corpus import stopwords
from gensim.models import KeyedVectors

import numpy as np


def strip_html_tags(html_text):
    
    tree = html.fromstring(html_text)
    clean_tree = clean_html(tree)
    result = clean_tree.text_content().strip()
    result = result.replace("\\n","").replace("\\t","").replace("\\r","")
    return result

def extract_keywords(text):
    return keywords(text, ratio=0.3).split('\n')

def summarize_content(text, ratio=0.2):
    return summarize(text, ratio)


def suggest_title(prefix):
    data = {
        'text': prefix
    }

    url = 'http://0.0.0.0:9091/1.0/natural-language-understanding/title-generator/'

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf8'))
    
    if("title" in result.keys()):
        suggested_title = result["title"].title()        
        return suggested_title
    
    return ""

def generate(prefix):
    data = {
        'text': prefix
    }

    url = 'http://0.0.0.0:9091/1.0/natural-language-understanding/text-generation/'

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    generated_text = json.loads(response.read().decode('utf8'))
    
    return generated_text

def similar_sentences(text):
    data = {
        'text': text
    }

    url = 'http://0.0.0.0:9091/1.0/natural-language-understanding/similar-sentences/'

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf8'))
    
    return result    

def classify_sentency_purpose(sentence):
    data = {
        'text': sentence
    }

    url = 'http://0.0.0.0:9091/1.0/natural-language-understanding/sentence-classifier/'

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    predictions = json.loads(response.read().decode('utf8'))
    
    return predictions

purpose_code = ["background","objective","methods","results","conclusions","unlabelled"]
def analyze_content_purpose(text):
    sent_text = nltk.sent_tokenize(text) # this gives us a list of sentences
    # now loop over each sentence and tokenize it separately

    result = [] 
    for sent_id,sentence in enumerate(sent_text):
        class_label = classify_sentency_purpose(sentence)[0][0]
        class_confidence = classify_sentency_purpose(sentence)[0][1]
        sentence
        result.append({
            "purpose":class_label,
            "purpose_code":purpose_code.index(class_label),
            "sentence":sentence,
            "sentence_order":sent_id,
            "confidence_score" : class_confidence
        })

    return result

    
def get_sentences_by_purpose(purpose_name,content_analyzed):
    purpose_sentences = []
    for analyzed_sentence in content_analyzed:
        if(analyzed_sentence["purpose"] == purpose_name):
            purpose_sentences.append(analyzed_sentence)
    return purpose_sentences

def organized_sentences_by_purposes(content_analyzed):
    background = get_sentences_by_purpose("background",content_analyzed)
    objective = get_sentences_by_purpose("objective",content_analyzed)
    methods = get_sentences_by_purpose("methods",content_analyzed)
    results = get_sentences_by_purpose("results",content_analyzed)
    conclusions = get_sentences_by_purpose("conclusions",content_analyzed)

    background = sorted(background, key=lambda k: k['sentence_order']) 
    objective = sorted(objective, key=lambda k: k['sentence_order']) 
    methods = sorted(methods, key=lambda k: k['sentence_order']) 
    results = sorted(results, key=lambda k: k['sentence_order']) 
    conclusions = sorted(conclusions, key=lambda k: k['sentence_order']) 

    combined_result = {
        "background":[ordered_sentence["sentence"] for ordered_sentence in background] ,
        "objective":[ordered_sentence["sentence"] for ordered_sentence in objective] ,
        "methods":[ordered_sentence["sentence"] for ordered_sentence in methods] ,
        "results":[ordered_sentence["sentence"] for ordered_sentence in results] ,
        "conclusions":[ordered_sentence["sentence"] for ordered_sentence in conclusions] 
        }

    return(combined_result)    

