from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import EditableHTML, Project
from flask import Flask, request, make_response

from flask import request, session
import urllib.request
import json    

from app import db
from .forms import SearchForm
from .utils import strip_html_tags, keywords, summarize, extract_keywords, summarize_content, similar_sentences
from .utils import analyze_content_purpose, classify_sentency_purpose, organized_sentences_by_purposes
#from .sentence_models import most_similar_sentence, load_my_sentence_model_corpus
#from .api import find_specialists, find_technical_definitions, search_by_query
from .utils import generate, suggest_title

import app.search.api_pubmed
import app.search.api_dspace_uporto
from app.models import Project, FavoritePaper , Note
from flask_login import current_user, login_required

from flask import url_for



search_api = Blueprint('search', __name__)

@search_api.route('/', methods=['POST','GET'])
@login_required
def index():

    favorites = FavoritePaper.query.filter_by(user_id=current_user.id)

    form = SearchForm(request.form)
    print("POST.search.session",session)
    result = {
        "hits":[],
        "total_hits":0,
        "offset":0,
        "limit":10,
        "sort_by":"recent",
        "repository":"pubmed",        
        }
    
    if (request.method == 'GET'):
        fquery = request.args.get('query', default = "", type = str)
        form.query.data = fquery        
        result["query"] = fquery
        result["offset"] = request.args.get('offset', default = 0, type = int)
        result["limit"] = request.args.get('limit', default = 10, type = int)
        result["sort_by"] = request.args.get('sort_by', default = "recent", type = str)
        result["repository"] = request.args.get('repository', default = "pubmed", type = str)

        if(result["repository"] not in ["pubmed","dspace_uporto","dspace_uminho"]):
            result["repository"] = "pubmed"

        if(fquery != None and fquery != ""):

            if(result["repository"] == "pubmed"):
                results, total = app.search.api_pubmed.search_by_query(result["query"], 
                                                result["offset"], 
                                                result["limit"],
                                                result["sort_by"],
                                                result["repository"])

            elif(result["repository"] in ["dspace_uporto","dspace_uminho"] ):
                print("search papers at",result["repository"])

                results, total = app.search.api_dspace_uporto.search_by_query(result["query"], 
                                                result["offset"], 
                                                result["limit"],
                                                result["sort_by"],
                                                result["repository"])

            result["hits"] = results 
            result["total_hits"] = total 

            next_page_offset = int(result["offset"]) + 10
            previous_page_offset = int(result["offset"]) - 10

            result["previous_page_url"] = url_for('search.index', query=fquery, 
                                                                  offset=previous_page_offset, 
                                                                  limit=10, 
                                                                  sort_by=result["sort_by"], 
                                                                  repository=result["repository"]) 

            result["next_page_url"] = url_for('search.index', query=fquery, 
                                                                offset=next_page_offset, 
                                                                limit=10, 
                                                                sort_by=result["sort_by"], 
                                                                repository=result["repository"]) 

    my_favorites_identifiers = [item.repository + "_" + item.identifier for item in favorites]
    return render_template('main/search.html', form=form, result=result, my_favorites=favorites, my_favorites_identifiers=my_favorites_identifiers)  

## AJAX REQUESTS
@search_api.route("/related_work/<repository>",methods=['POST',"OPTIONS"])
def api_related_work(repository="pubmed"):
    print("chamando api_related_work")
    text = request.data 
    text = str(text, 'utf-8')
    print("text",text)
    if(repository not in ["pubmed","dspace_uporto","dspace_uminho"]):
        repository = "pubmed"
    
    related_terms = text
    if(len(text.split()) >= 15):
        text = strip_html_tags(text)
        keywords = extract_keywords(text)
        related_terms = ",".join(keywords)
    
    results = []
    if(repository == "pubmed"):
        results, total = app.search.api_pubmed.search_by_query(query=related_terms,
                                                                offset=0,
                                                                limit=10,
                                                                sort_by="recent",
                                                                repository=repository)
    if(repository in ["dspace_uporto","dspace_uminho"]):
        results, total = app.search.api_dspace_uporto.search_by_query(query=related_terms,
                                                                offset=0,
                                                                limit=10,
                                                                sort_by="recent",
                                                                repository=repository)

    
    return json.dumps(results,indent=4)


@search_api.route("/specialists/<repository>", methods=['POST'])
def api_find_specialists(repository=None):
    text = request.data 
    text = str(text, 'utf-8')

    if(repository not in ["pubmed","dspace_uporto","dspace_uminho"]):
        repository = "pubmed"
    
    
    related_terms = text
    if(len(text.split()) >= 15):
        text = strip_html_tags(text)
        keywords = extract_keywords(text)
        related_terms = ",".join(keywords)

    

    print("related_terms",related_terms)
    
    results = []
    if(repository == "pubmed"):
        results = app.search.api_pubmed.find_specialists(related_terms, repository=repository)
    
    if(repository in ["dspace_uporto","dspace_uminho"]):
        results = app.search.api_dspace_uporto.find_specialists(related_terms, repository=repository)
    
    print(len(results))
    #response = search_api.response_class(
    #    response=json.dumps(results,indent=4),
    #    status=200,
    #    mimetype='application/json'
    #)
    
    return json.dumps(results,indent=4)

@search_api.route("/definitions/",methods=['POST'])
def api_find_technical_definitions():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("extract_keywords",text)
    results = app.search.api_pubmed.find_technical_definitions(text)
    
    """ response = search_api.response_class(
        response=json.dumps(results,indent=4),
        status=200,
        mimetype='application/json'
    ) """
    
    return json.dumps(results,indent=4)

@search_api.route('/remove-favorite', methods=['GET'])
@login_required
def delete_favorite():
    identifier = request.args.get('identifier')
    repository = request.args.get('repository')

    favpaper = FavoritePaper.query.filter_by(identifier=identifier,repository=repository).first()
    if(favpaper):
        db.session.delete(favpaper)
        db.session.commit()

    resp = make_response()
    resp.status_code = 201
    resp.headers['Access-Control-Allow-Origin'] = '*'
    #flash('Favorite paper {} successfully persisted'.format(favorite.title),'form-success')

    #return redirect('dashboard')
    return resp

@search_api.route('/remove-note', methods=['GET'])
@login_required
def delete_note():
    note_id = request.args.get('id')
    identifier = request.args.get('identifier')
    repository = request.args.get('repository')

    note = Note.query.filter_by(identifier=identifier, repository=repository, id=note_id).first()
    if(note):
        db.session.delete(note)
        db.session.commit()

    resp = make_response()
    resp.status_code = 201
    resp.headers['Access-Control-Allow-Origin'] = '*'
    #flash('Favorite paper {} successfully persisted'.format(favorite.title),'form-success')

    #return redirect('dashboard')
    return resp    


@search_api.route('/add-favorite', methods=['POST'])
@login_required
def new_favorite():
    """Create a new project."""

    print (request.is_json)
    print (request.data)
    
    form = json.loads(request.data)
    
   # try:
    
    if(form["is_favorite"] == 0):
        favpaper = FavoritePaper.query.filter_by(identifier=form["identifier"],repository=form["repository"]).first()
        if(favpaper):
            db.session.delete(favpaper)
            db.session.commit()
    else:

        favorite = FavoritePaper(
            identifier=form["identifier"],
            repository=form["repository"]
          #  document_id=form["document_id"],
        )

        if("title" in form):
            favorite.title=form["title"]
        if("authors" in form):
            favorite.abstract=form["authors"]
        if("abstract" in form):
            favorite.abstract=form["abstract"]
        if("pubdate" in form):
            favorite.pubdate=form["pubdate"]
        if("url" in form):
            favorite.url=form["url"]
        if("pdf_url" in form):
            favorite.pdf_url=form["pdf_url"]
        if("has_pdf_content" in form):
            favorite.has_pdf_content=form["has_pdf_content"]
        

        favorite.user_id = current_user.id
        

        db.session.add(favorite)
        db.session.commit()

    resp = make_response()
    resp.status_code = 201
    resp.headers['Access-Control-Allow-Origin'] = '*'
    #flash('Favorite paper {} successfully persisted'.format(favorite.title),'form-success')

    #return redirect('dashboard')
    return resp
   
   # except:
   #     resp = make_response(json.dumps({"error":"failed to persist favorite paper"}))
   #     resp.status_code = 500
   #     resp.headers['Access-Control-Allow-Origin'] = '*'
   #     return resp

    #return render_template('admin/new_project.html', form=form)

@search_api.route("/analyze_content_purpose/",methods=['POST'])
def api_analyze_content_purpose():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("analyze_content_purpose",text)
    
    my_content_analyzed = analyze_content_purpose(text)
    results = organized_sentences_by_purposes(my_content_analyzed)    
    print(len(results))
    # response = app.response_class(
    #     response=json.dumps(results,indent=4),
    #     status=200,
    #     mimetype='application/json'
    # )
    
    # return response

    return json.dumps(results,indent=4)

@search_api.route("/analyze_content_purpose_detailed/",methods=['POST'])
def api_analyze_content_purpose_detailed():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("analyze_content_purpose",text)
    
    results = analyze_content_purpose(text)
    print(results)
        
    # print(len(results))
    # response = app.response_class(
    #     response=json.dumps(results,indent=4),
    #     status=200,
    #     mimetype='application/json'
    # )
    
    # return response  
    return json.dumps(results,indent=4)

@search_api.route("/summarize/",methods=['POST'])
def api_summarize():
    text = request.data 
    text = str(text, 'utf-8')
    
    print("summarize text", text)
    text = strip_html_tags(text)
    
    try:
        return summarize_content(text)    
    except:
        
        resp = make_response()
        resp.status_code = 201
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #flash('Favorite paper {} successfully persisted'.format(favorite.title),'form-success')

        #return redirect('dashboard')
        return resp
    

@search_api.route("/similar_sentences/",methods=['POST'])
def api_most_similar():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("most_similar",text)
    
    results = []
    for sent in  similar_sentences(text):
        results.append(sent)
        
    print(len(results))
    # response = app.response_class(
    #     response=json.dumps(results,indent=4),
    #     status=200,
    #     mimetype='application/json'
    # )
    return json.dumps(results,indent=4)


@search_api.route("/generate/",methods=['POST'])
def api_generate():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("generate text using",text)
    
    results = generate(text)
        
    print(len(results))
    # response = app.response_class(
    #     response=json.dumps(results,indent=4),
    #     status=200,
    #     mimetype='application/json'
    # )
    return json.dumps(results,indent=4)    


@search_api.route("/suggest_title/",methods=['POST'])
def api_suggest_title():
    text = request.data 
    text = str(text, 'utf-8')
    
    text = strip_html_tags(text)
    print("suggest title for text: ",text)
    
    results = suggest_title(text)
        
    print(len(results))
    # response = app.response_class(
    #     response=json.dumps(results,indent=4),
    #     status=200,
    #     mimetype='application/json'
    # )
    return json.dumps(results,indent=4)        
