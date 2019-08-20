
from lxml import html
from lxml.html.clean import clean_html

import urllib.request
import json    

import nltk
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize

from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from sklearn.preprocessing import normalize
import numpy as np

en_stopwords = nltk.corpus.stopwords.words('english')


en_model = None
loaded_model = None
loaded_corpus = None

def load_en_w2v_model():
    # Loading sentence model
    global en_model
    print("loading pretreined word embeddings model...")
    if (en_model == None):
        en_model = KeyedVectors.load_word2vec_format('./models/wiki-news-300d-1M.vec')
    
    return en_model
    
def load_my_sentence_model():
    print("loading pretreined sentence model...")
    global loaded_model
    print(type(loaded_model))
    if (loaded_model is None):
        loaded_model = np.load('./models/background_sentence_model_v2.npz')["model"]
        print(loaded_model.shape)

    return loaded_model

def load_my_sentence_model_corpus():
    global loaded_corpus 
    if (loaded_corpus  is None):
        loaded_corpus = np.load('./models/background_sentence_corpus_v2.npz')["corpus"]
        print("models loaded")
        print(loaded_corpus.shape)
        
    return loaded_corpus

def sentence_to_vec(sentence, normalize=False):
    words = [word for word in sentence.split()]
    
    # Remove their stopwords.    
    words = [w for w in words if w not in en_stopwords]
            
    #vectors = [en_model.word_vec(word) for word in words]
    vectors = []
    for word in words:
        try:
            vectors.append(load_en_w2v_model().word_vec(word))
        except:
            print(word,"not in vocab")
            continue
           
    
    sentence_vector = np.mean(vectors, axis=0)
    
    if(normalize):
        sentence_vector = np.array(sentence_vector)
        sentence_vector = normalize([sentence_vector], norm='l2', axis=1)[0]
    
    return sentence_vector

def most_similar_sentence(search, topN=1):
    load_en_w2v_model()
    load_my_sentence_model()
    load_my_sentence_model_corpus()

    query = sentence_to_vec(search)
    query = np.array(query)
    query = normalize([query], norm='l2', axis=1)[0]
    
    sims = np.dot(load_my_sentence_model(), query)
    top_sims = np.argsort(sims)[::-1][:topN]
    return top_sims    