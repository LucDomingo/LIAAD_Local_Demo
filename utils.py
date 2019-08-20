from lxml import html
from lxml.html.clean import clean_html

import urllib.request
import json    

import nltk
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize

from nltk.corpus import stopwords
from gensim.models import KeyedVectors

from tools.pampo.pampo.ner import extract_entities
from tools.contamehistorias.datasources.webarchive import ArquivoPT
from tools.contamehistorias import engine
import tools.yake.yake as yake
from tools.yake.yake import KeywordExtractor
from textblob import TextBlob
import langid
from flask import jsonify
import re
import nltk
nltk.download('punkt')



import numpy as np
from datetime import datetime


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
    

purpose_code = ["background","objective","methods","results","conclusions","unlabelled","unassigned"]
def analyze_content_purpose(text):
    sent_text = nltk.sent_tokenize(text) # this gives us a list of sentences
    # now loop over each sentence and tokenize it separately
    result = [] 
    for sent_id,sentence in enumerate(sent_text):
        class_label = classify_sentency_purpose(sentence)[0][0]
        class_confidence = classify_sentency_purpose(sentence)[0][1]
        sentence
        result.append((class_label,sentence,class_confidence))

    return result

    
def get_sentences_by_purpose(purpose_name,content_analyzed):
    purpose_sentences = []
    for analyzed_sentence in content_analyzed:
        if(analyzed_sentence["purpose"] == purpose_name):
            purpose_sentences.append(analyzed_sentence)
    return purpose_sentences

def organized_sentences_by_purposes(content_analyzed,original):
    background = get_sentences_by_purpose("background",content_analyzed)
    objective = get_sentences_by_purpose("objective",content_analyzed)
    methods = get_sentences_by_purpose("methods",content_analyzed)
    results = get_sentences_by_purpose("results",content_analyzed)
    conclusions = get_sentences_by_purpose("conclusions",content_analyzed)
    unassigned = get_sentences_by_purpose("unassigned",content_analyzed)

    sent_text = nltk.sent_tokenize(text)

    background = sorted(background, key=lambda k: k['sentence_order']) 
    objective = sorted(objective, key=lambda k: k['sentence_order']) 
    methods = sorted(methods, key=lambda k: k['sentence_order']) 
    results = sorted(results, key=lambda k: k['sentence_order']) 
    conclusions = sorted(conclusions, key=lambda k: k['sentence_order'])
    unassigned = sorted(unassigned, key=lambda k: k['sentence_order'])

    combined_result = {
        "background":[ordered_sentence["sentence"] for ordered_sentence in background] ,
        "objective":[ordered_sentence["sentence"] for ordered_sentence in objective] ,
        "methods":[ordered_sentence["sentence"] for ordered_sentence in methods] ,
        "results":[ordered_sentence["sentence"] for ordered_sentence in results] ,
        "conclusions":[ordered_sentence["sentence"] for ordered_sentence in conclusions],
        "unassigned":[ordered_sentence["sentence"] for ordered_sentence in unassigned] 
        }

    return(combined_result) 


def response_json(pred,data,model):
        model_predictor = pred[model]

        if model=="pampo":
            pampo=pred[model]
            keywords1="No text given"
            keywords2="No demo text given"
            try:
                dt=data['user']
                keywords1 = pampo(dt)
            except:
                pass
            
            try:
                dt=data['select']
                keywords2 = pampo(dt)
            except:
                pass
            

            output={'user':"",'select':""}
            output['user']=keywords1
            output['select']=keywords2

        elif model=="conta":
            start_date=""
            end_date=""
            domain=data['domain']

            try:
                

                start_date= (data['date'][0])[0:10]+" 00:00:00"
                end_date= (data['date'][1])[0:10]+" 00:00:00"

                start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

 
            except:
                pass
            try:
                frame=data['radio1']
                date=""
                if(frame=='five'):
                    date = datetime.now()
                    begin=int(date.year)-5
                    date = date.replace(year=begin)
                if(frame=='ten'):
                    date = datetime.now()
                    begin=int(date.year)-10
                    date = date.replace(year=begin)
                if(frame=='fifteen'):
                    date = datetime.now()
                    begin=int(date.year)-15
                    date = date.replace(year=begin)
                end_date = datetime.now()
                start_date = date
            except:
                pass


            params = { 'domains':domain, 
                'from':start_date, 
                'to':end_date }
            query=data['keywords']
            apt =  pred[model]()
            search_result = apt.getResult(query=query, **params)
            cont = engine.TemporalSummarizationEngine()
            intervals = cont.build_intervals(search_result, "pt")
            out=cont.pprint(intervals)
            output={'text':"","date":[],"article":[]}
            output['text']=out[0]
            output['date']=out[1][0]
            output['article']=out[1][1]
                
        elif model=="yake":
            func=pred[model]()
            keywords1="No text given"
            keywords2="No demo text given"
            original1=""
            original2=""
            origin=""
            try:
                dt=data['user']
                n=int(data['slider1'])
                top=int(data['slider2'])
                
                custom_kwextractor = yake.KeywordExtractor(lan="en", n=n, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=top, features=None)
                keywords1 = custom_kwextractor.extract_keywords(dt)
                temp=[]
                tempup=[]
                for i in range (0,len(keywords1)):
                    temp.append(keywords1[i][0])
                    tempup.append(keywords1[i][0].title())
                original1=dt
                origin="("+"|".join(temp+tempup)+")" 
                original1=re.split(origin,original1)
            except:
                pass
            
            try:
                lan=data['select'][0:2]
                dt=data['select'][3:]
                n=data['slider1']
                top=data['slider2']
                custom_kwextractor = yake.KeywordExtractor(lan=lan, n=n, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=top, features=None)
                keywords2 = custom_kwextractor.extract_keywords(dt)

                temp=[]
                tempup=[]
                for i in range (0,len(keywords2)):
                    temp.append(keywords2[i][0])
                    tempup.append(keywords2[i][0].title())
                original2=dt
                origin="("+"|".join(temp+tempup)+")" 
                original2=re.split(origin,original2)
            except:
                pass

            output={'user':"",'select':"","original1":"","original2":""}
            output['user']=keywords1

            output['select']=keywords2
            output['original1']=original1
            output['original2']=original2


        elif model=="sentiment_analyser":
            result={}
            sentiment = pred[model](data['text']).sentiment

            output={'polarity':"",'subjectivity':""}
            output['polarity'] = str(round(sentiment.polarity,2))
            output['subjectivity'] =str (round(sentiment.subjectivity,2))
        elif model=="generate":
            text = data["text"]  
            text = strip_html_tags(text)
            results = pred[model](text)
            output={'original':"",'result':""}
            output['result']=results
            output['original']=text
        elif model=="title":
            text = data["text"]
            text = strip_html_tags(text)
            results = pred[model](text)
            output={'original':"",'result':""}
            output['result']=results
            output['original']=text
        elif model=="similar":
            text = data["text"]
            text = strip_html_tags(text)    
            results = []
            for sent in  pred[model](text):
                results.append(sent)
            output={'result':""}
            output['result']=results         
        elif model=="summarization":
            text = data["text"]
            text = strip_html_tags(text)   
            output={'result':""}
            output['result']=pred[model](text)   
        elif model=="language_detection":
            text = data["text"]
            output={'result':""}
            output['result']=langid.classify(text)[0] 
        elif model=="classify":
            output={"result":[]}
            try:
                dt=data['user']
            except:
                dt=data['select']
            my_content_analyzed = analyze_content_purpose(dt)
            print(my_content_analyzed)
            output['result']=my_content_analyzed


        return output
