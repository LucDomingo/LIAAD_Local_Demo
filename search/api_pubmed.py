import numpy as np
from random import randint
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib.request
import json    

def get_document_by_id(identifier, repository="pubmed"):
    print("get_document_by_id",repository, identifier)
    es = Elasticsearch("http://localhost:9200")

    if(repository not in ["pubmed","dspace_uporto"]):
        repository = "pubmed"



    if(identifier and identifier != ""):
        #get first
        # res = es.search(index=repository, request_timeout=60, 
        #                         body={
        #                             "size" : 1,
        #                             'query': { 
        #                                   "bool": {
        #                                     "must": {
        #                                         "term": {"pmid": identifier}
        #                                         #"term": {"repository": repository}
                                                 
        #                                     }
        #                                   }
        #                             }})
        hit = es.get(index=repository, request_timeout=60, id=identifier, doc_type="paper")

        #print("Got %d Hits:" % res['hits']['total'])
        print("Got hit?",hit)
        #get first
        #for hit in res['hits']['hits']:
        if(hit):
            print(hit)

            title = hit["_source"]["title"]
            title = title.encode().decode("utf8")
            title = title.replace("["," ").replace("]"," ").replace("."," ").replace("\n"," ").replace("\t"," ").strip()
            abstract = hit["_source"]["abstract"].encode().decode("utf8")
            abstract = abstract.replace("\n"," ").replace("\t"," ").strip()
            doc = {
                    "repository":"pubmed",
                    "identifier":hit["_source"]["pmid"],
                    "title":title,
                    "abstract":abstract,
                    "authors":hit["_source"]["author"],
                    "pubdate":hit["_source"]["pubdate"],
                    "venue":hit["_source"]["journal"],
                    #"document_id":hit["_id"]                        
                    }
            
            doc["url"] = "https://www.ncbi.nlm.nih.gov/pubmed/" +  hit["_source"]["pmid"]

            return doc

    return None

def search_by_query(query, offset=0, limit=10, sort_by="recent", repository="pubmed"):
    results = []
    es_related_work = Elasticsearch("http://localhost:9200")

    if(sort_by == "recent"):
        sort_by = "desc"
    else:
        sort_by = "asc"

    if(repository not in ["pubmed","dspace_uporto"]):
        repository = "pubmed"

    res = es_related_work.search(index=repository, request_timeout=60, 
                                 body={
                                    # e preciso definir no schema o pubdate como fielddata=true
                                    #  "sort" : [
                                    #     { "pubdate" : {"order" : sort_by}},
                                    #     "_score"
                                    # ],
                                     "from" : offset, "size" : limit,
                                     'query': { 
                                      "multi_match" : {
                                        "query":    query, 
                                        "fields": [ "title^3", "abstract" ] 
                                        }
                                 }
                                })
     
    print("Got %d Hits:" % res['hits']['total'])
    
    for hit in res['hits']['hits']:
        print("----------------------")
        print(hit["_source"])
        title = hit["_source"]["title"]
        title = title.encode().decode("utf8")
        title = title.replace("["," ").replace("]"," ").replace("."," ").replace("\n"," ").replace("\t"," ").strip()
        abstract = hit["_source"]["abstract"].encode().decode("utf8")
        abstract = abstract.replace("["," ").replace("]"," ").replace("."," ").replace("\n"," ").replace("\t"," ").strip()
            
        doc = {
                "document_id":hit["_id"],
                "repository":"pubmed",
                "identifier":hit["_source"]["pmid"],
                "title":title,
                "abstract":abstract,
                "authors":hit["_source"]["author"],
                "pubdate":hit["_source"]["pubdate"],
                "venue":hit["_source"]["journal"]
                  }
        
        doc["url"] = "https://www.ncbi.nlm.nih.gov/pubmed/" +  hit["_source"]["pmid"]

        results.append(doc)
    
    return results, res['hits']['total']    

def find_technical_definitions(query):
    print("find_technical_definitions",query)
    results = []

    es_concepts = Elasticsearch("http://localhost:9200")
    res = es_concepts.search(index="mesh_concepts", 
                                    request_timeout=60, 
                                    body={                                     
                                    "query": {
                                        "match" : {
                                            "concept_name" : str(query)
                                        }
                                    }
                                })
     
    print("Got %d Hits:" % res['hits']['total'])
    
    for hit in res['hits']['hits']:
       
        concept_name = hit["_source"]["concept_name"]
        concept_name = concept_name.encode().decode("utf8")
        
        concept_scope_note =  hit["_source"]["concept_scope_note"]
        concept_scope_note = concept_scope_note.encode().decode("utf8")
        doc = {
                "concept_ui":hit["_source"]["concept_ui"],
                "concept_name":concept_name,
                "concept_scope_note":concept_scope_note
                  }
        
        print(doc["concept_name"])
        results.append(doc)
        print("########################")
    
    return results

def find_specialists(query, repository="pubmed"):
    es_specialists = Elasticsearch("http://localhost:9200")
    specialists = []
    res = es_specialists.search(index=repository,request_timeout=160,  body={
      "size":0,
         "query": {
            "match" : {
                "abstract" : query
            }
        },    
      "aggs": {
        "top_authors": {
          "terms": { 
            "field": "author.raw",
            "size":15      
          }
        }
      }
    })

    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['aggregations']["top_authors"]["buckets"]:
        print(hit)
        specialists.append(hit)
    
    return specialists    