import urllib.request
import json
import base64
import binascii
import re
from lxml import html
from lxml.html.clean import clean_html
import nltk
nltk.download('punkt')

from datetime import datetime

def strip_html_tags(html_text):
    
    tree = html.fromstring(html_text)
    clean_tree = clean_html(tree)
    result = clean_tree.text_content().strip()
    result = result.replace("\\n","").replace("\\t","").replace("\\r","")
    return result

def summarize_content(text, ratio=0.2):
    return summarize(text, ratio)


def suggest_title(prefix):
    data = {
        'text': prefix
    }

    url = 'http://liaadnlpserver:9091/1.0/natural-language-understanding/title-generator/'

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

    url = 'http://liaadnlpserver:9091/1.0/natural-language-understanding/text-generation/'

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

    url = 'http://liaadnlpserver:9091/1.0/natural-language-understanding/similar-sentences/'

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

    url = 'http://liaadnlpserver:9091/1.0/natural-language-understanding/sentence-classifier/'

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


def response_json(data,model):

        output={'user':"",'select':""}

        if model=="pampo":
            keywords1="No text given"
            keywords2="No demo text given"
            url = 'http://pypamposvc:8000/pampo'
            try:
                dt=data['user']
                data = {'text': dt}
                params = json.dumps(data).encode('utf8')
                req = urllib.request.Request(url, data=params,headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                predictions = json.loads(response.read().decode('utf8'))            
                keywords1 = predictions
                origin="("+"|".join(keywords1)+")" 
                dt=re.split(origin,dt)
                keywords2 = {'text':dt,'tokens':keywords1}
            except Exception as e:
                print(e)
                       
            try:
                dt=data['select']
                data = {'text': dt}
                params = json.dumps(data).encode('utf8')
                req = urllib.request.Request(url, data=params,headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                predictions = json.loads(response.read().decode('utf8'))                
                keywords2 = predictions
                origin="("+"|".join(keywords2)+")" 
                dt=re.split(origin,dt)
                keywords2 = {'text':dt,'tokens':keywords2}
            except Exception as e:
                print(e)
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
                end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
                start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
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
                end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                start_date = date.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
            url='http://contamehistoriassvc:8000/conta'
            params = { 'domains':domain,'query':data['keywords'],
                'start_date':start_date, 
                'end_date':end_date}
            params = json.dumps(params).encode('utf8')
            req = urllib.request.Request(url, data=params,headers={'content-type': 'application/json'})
            response = urllib.request.urlopen(req)
            out = json.loads(response.read().decode('utf8')) 
            output={'text':"","date":[],"article":[]}
            output['text']=out[0]
            output['date']=out[1][0]
            output['article']=out[1][1]

        elif model=="generate":
            text = data["text"]  
            text = strip_html_tags(text)
            results = generate(text)
            output={'original':"",'result':""}
            output['result']=results
            output['original']=text
        elif model=="title":
            text = data["text"]
            text = strip_html_tags(text)
            results = suggest_title(text)
            output={'original':"",'result':""}
            output['result']=results
            output['original']=text      
        elif model=="summarization":
            text = data["text"]
            text = strip_html_tags(text)   
            output={'result':""}
            output['result']=summarize_content(text)
        elif model=="classify":
            output={"result":[]}
            try:
                dt=data['user']
            except:
                dt=data['select']
            my_content_analyzed = analyze_content_purpose(dt)
            output['result']=my_content_analyzed
        elif model=="yake":
            keywords1="No text given"
            keywords2="No demo text given"
            original1=""
            original2=""
            origin=""
            lan="en"
            url='http://yakesvc:8000/yake'
            try:
                dt=data['user']
                n=int(data['slider1'])
                top=int(data['slider2'])
                params = { 'text':dt,'language':lan,
                'max_ngram_size':n, 
                'number_of_keywords':top}
                params = json.dumps(params).encode('utf8')
                req = urllib.request.Request(url, data=params,headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                keywords1 = json.loads(response.read().decode('utf8'))                              
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
                params = { 'text':dt,'language':lan,
                'max_ngram_size':n, 
                'number_of_keywords':top}
                params = json.dumps(params).encode('utf8')
                req = urllib.request.Request(url, data=params,headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                keywords2 = json.loads(response.read().decode('utf8'))

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
        return output
def int_to_slug(i: int) -> str:
    """
    Turn an integer id into a semi-opaque string slug
    to use as the permalink.
    """
    byt = str(i).encode('utf-8')
    slug_bytes = base64.urlsafe_b64encode(byt)
    return slug_bytes.decode('utf-8')

def slug_to_int(slug: str):
    """
    Convert the permalink slug back to the integer id.
    Returns ``None`` if slug is not well-formed.
    """
    byt = slug.encode('utf-8')
    try:
        int_bytes = base64.urlsafe_b64decode(byt)
        return int(int_bytes)
    except (binascii.Error, ValueError):
        logger.error("Unable to interpret slug: %s", slug)
        return None
