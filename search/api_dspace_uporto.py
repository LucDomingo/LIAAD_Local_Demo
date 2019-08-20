import numpy as np
from random import randint
from datetime import datetime
from elasticsearch import Elasticsearch
import urllib.request
import json    

def get_document_by_id(identifier, repository="dspace_uporto"):
    print("get_document_by_id",repository, identifier)
    es = Elasticsearch("http://localhost:9200")

    if(repository not in ["pubmed","dspace_uporto","dspace_uminho"]):
        repository = "dspace_uporto"



    if(identifier and identifier != ""):
        #get first
        #print("http://localhost:9200/"+repository+"/_search")
        hit = es.get(index=repository, request_timeout=60, id=identifier, doc_type="paper")

        print("Found hit?",hit)
    
        #get first
        if(hit):
            
            title = hit["_source"]["title"]
            title = title.encode().decode("utf8")
            title = title.replace("["," ").replace("]"," ").replace("."," ").strip()
            doc = {
                    "repository":repository,
                    "identifier":hit["_source"]["identifier"],
                    "title":title,
                    "authors":hit["_source"]["creators"],
                    "pubdate":hit["_source"]["datestamp"],
                    "url":hit["_source"]["identifier_uri"]
                    }

            doc["abstract"] = ""

            if("description_abstract" in hit["_source"].keys()):
                doc["abstract"] = hit["_source"]["description_abstract"]

            doc["authors"] = doc["authors"]
            doc["pubdate"] = doc["pubdate"].split("-")[0] #get year
            #doc["abstract"] =""
            doc["venue"] = ""
            doc["files"] = []

            if(len(hit["_source"]["specs"]) > 0):
                #if("name" in hit["_source"]["specs"].keys()):
                doc["venue"] = hit["_source"]["specs"][0]["name"]
            
            doc["has_pdf_content"] = hit["_source"]["has_pdf_content"]
            doc["files_urls"] = hit["_source"]["attachments_urls"]

            return doc

    return None

def search_by_query(query, offset=0, limit=10, sort_by="recent", repository="dspace_uporto"):
    results = []
    es_related_work = Elasticsearch("http://localhost:9200")

    if(sort_by == "recent"):
        sort_by = "desc"
    else:
        sort_by = "asc"

    if(repository not in ["pubmed","dspace_uporto","dspace_uminho"]):
        repository = "dspace_uporto"

    body_query = {
                                    # e preciso definir no schema o pubdate como fielddata=true
                                    #  "sort" : [
                                    #     { "pubdate" : {"order" : sort_by}},
                                    #     "_score"
                                    # ],
                                     "_source": {
                                        "excludes": [ "content" ]
                                    },

                                     "from" : offset, "size" : limit,
                                     'query': {
                                          "bool": {
                                              "must": {
                                                "multi_match" : {
                                                   "query":    query,
                                                   "fields": [ "title^5", "description_abstract", "content","abstract","subjects^2" ]
                                                }
                                              },
                                              "filter": {
                                                "bool" : {
                                                    "must" : [
                                                        {"term": {"rights": "openaccess"}},
                                                        {"term": {"has_pdf_content": True}}
                                                      ]
                                                }
                                              }
                                          }
                                     }
                                }

    print(body_query)

    res = es_related_work.search(index=repository, 
                                 request_timeout=60,
                                 body=body_query
                                )

    print("results from ",repository) 
    print("Got %d Hits:" % res['hits']['total'])
    
    for hit in res['hits']['hits']:
        print("----------------------")
        print(hit)
        title = hit["_source"]["title"]
        title = title.encode().decode("utf8")
        title = title.replace("["," ").replace("]"," ").replace("."," ").strip()
        print("hit.rights",hit["_source"]["rights"])

        doc = {
                "repository":repository,
                "identifier":hit["_source"]["identifier"],
                "title":title,
                "authors":hit["_source"]["creators"],
              #  "abstract":hit["_source"]["description_abstract"],
                "pubdate":hit["_source"]["datestamp"],
                "url":hit["_source"]["identifier_uri"]
                  }
        doc["authors"] = doc["authors"]
        doc["pubdate"] = doc["pubdate"].split("-")[0] #get year
        doc["abstract"] = ""
        doc["venue"] = ""
        doc["files"] = []

        if(len(hit["_source"]["specs"]) > 0):
            #if("name" in hit["_source"]["specs"].keys()):
            doc["venue"] = hit["_source"]["specs"][0]["name"]
        
        doc["has_pdf_content"] = hit["_source"]["has_pdf_content"]
        if("attachments_urls" in hit["_source"].keys()):
            doc["files_urls"] = hit["_source"]["attachments_urls"]
        
        #date_available
        #title
        #venue = specs[0]["name"]
        #attachments_urls = attachments_urls[0]
        #has_pdf_content
        #pub_type
        #language
        #identifier_uri
        #creators

        results.append(doc)
    
    return results, res['hits']['total']    

def find_technical_definitions(query):
    print("find_technical_definitions",query)
    results = []

    es_concepts = Elasticsearch("http://localhost:9200")
    res = es_concepts.search(index="mesh_concepts", body={                                     
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

def find_specialists(query, repository="dspace_uporto"):
    es_specialists = Elasticsearch("http://localhost:9200")
    specialists = []
    res = es_specialists.search(index=repository, body={
       "size":0,
         "query": {
            "match" : {
                "title" : query
            }
        },    
      "aggs": {
        "top_authors": {
          "terms": { 
            "field": "creators_raw",
            "size":15      
          }
        }
      }
    })

    print("Got %d Hits:" % res['hits']['total'])
    print(res)
    for hit in res['aggregations']["top_authors"]["buckets"]:
        print(hit)
        specialists.append(hit)
    
    return specialists    
