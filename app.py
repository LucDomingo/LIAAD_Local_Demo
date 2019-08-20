#!/usr/bin/env python
from datetime import datetime
from typing import Dict, Optional, List, Iterable
import argparse
import json
import os
import sys
import time
from functools import lru_cache
import re
from bson.objectid import ObjectId


import sys


from flask import Flask, request, Response, jsonify, send_file, send_from_directory
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from werkzeug.contrib.fixers import ProxyFix

from tools.pampo.pampo.ner import extract_entities
from tools.contamehistorias.datasources.webarchive import ArquivoPT
from tools.contamehistorias import engine
import tools.yake.yake as yake
from tools.yake.yake import KeywordExtractor
from textblob import TextBlob
import langid
from pymongo import MongoClient

from utils import strip_html_tags, keywords, summarize, extract_keywords, summarize_content, similar_sentences, analyze_content_purpose, classify_sentency_purpose, organized_sentences_by_purposes,generate, suggest_title,response_json

import psycopg2

import pytz

from server.permalinks import int_to_slug, slug_to_int
from server.db import DemoDatabase, PostgresDemoDatabase
from server.logging import StackdriverJsonFormatter
from server.models import DemoModel, load_demo_models


class ServerError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_dict = dict(self.payload or ())
        error_dict['message'] = self.message
        return error_dict

def main(demo_dir: str,
         port: int) -> None:
    """Run the server programatically"""

    # This will be ``None`` if all the relevant environment variables are not defined or if
    # there is an exception when connecting to the database.
    client = MongoClient('mongodb://localhost:27017')
    db = client.pymongo_test
    app = make_app(build_dir=f"{demo_dir}/build", demo_db=db)
    CORS(app)

    http_server = WSGIServer(('0.0.0.0', port), app)

    http_server.serve_forever()


def make_app(build_dir: str,
             demo_db: Optional[DemoDatabase] = None) -> Flask:
    if not os.path.exists(build_dir):
        sys.exit(-1)

    app = Flask(__name__)  # pylint: disable=invalid-name
    start_time = datetime.now(pytz.utc)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    
    app.pred={'pampo':extract_entities,'conta':ArquivoPT,'yake':KeywordExtractor,'sentiment_analyser':TextBlob,'generate':generate,'title':suggest_title,'similar':similar_sentences,'summarization':summarize_content,'classify':""}



    app.predictors = {}
    app.max_request_lengths = {} # requests longer than these will be rejected to prevent OOME
    app.wsgi_app = ProxyFix(app.wsgi_app) # sets the requester IP with the X-Forwarded-For header



    @app.errorhandler(ServerError)
    def handle_invalid_usage(error: ServerError) -> Response:  # pylint: disable=unused-variable
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route('/')
    def index() -> Response: # pylint: disable=unused-variable
        return send_file(os.path.join(build_dir, 'index.html'))

    @app.route('/permadata', methods=['POST', 'OPTIONS'])
    def permadata() -> Response:  # pylint: disable=unused-variable
        if request.method == "OPTIONS":
            return Response(response="", status=200)
        slug = request.get_json()["slug"]
        posts = demo_db.posts
        result=posts.find({ "slug": slug})

        for x in result:
            out=x 
        return jsonify({
                "modelName": out['model'],
                "requestData": out['request_data'],
                "responseData": out['response_data']
        })

    @app.route('/predict/<model_name>', methods=['POST', 'OPTIONS'])
    def predict(model_name: str) -> Response:  # pylint: disable=unused-variable
        if request.method == "OPTIONS":
            return Response(response="", status=200)
        
        data = request.get_json()
   
        model = model_name.lower()




        output=response_json(app.pred,data,model)

        posts = demo_db.posts
        post_data ={"response_data":output,
                    "slug":"",
                    "model":model_name,
                    "request_data":data}
        result_id = posts.insert_one(post_data).inserted_id
        myquery = { "_id": result_id }
        slug=int_to_slug(result_id)
        newvalues = { "$set": { "slug": slug } }
        output['slug']=slug
        print(posts.update_one(myquery, newvalues))



        return jsonify(output)
    @app.route('/', defaults={ 'path': '' })
    @app.route('/<path:path>')
    def static_proxy(path: str) -> Response: # pylint: disable=unused-variable
        if os.path.isfile(os.path.join(build_dir, path)):
            return send_from_directory(build_dir, path)
        else:
            # Send the index.html page back to the client as a catch-all, since
            # we're an SPA and JavaScript acts to handle routes the server
            # doesn't.
            return app.send_static_file('index.html')

    @app.route('/static/js/<path:path>')
    def static_js_proxy(path: str) -> Response: # pylint: disable=unused-variable
        return send_from_directory(os.path.join(build_dir, 'static/js'), path)

    @app.route('/static/css/<path:path>')
    def static_css_proxy(path: str) -> Response: # pylint: disable=unused-variable
        return send_from_directory(os.path.join(build_dir, 'static/css'), path)

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser("start the liaad tools demo")
    parser.add_argument('--port', type=int, default=8000, help='port to serve the demo on')
    parser.add_argument('--demo-dir', type=str, default='demo/', help="directory where the demo HTML is located")

    args = parser.parse_args()


    main(demo_dir=args.demo_dir,
         port=args.port)
