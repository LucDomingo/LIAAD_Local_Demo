#!/usr/bin/env python
from datetime import datetime
from typing import Dict, Optional, List, Iterable
import argparse
import json
import os
import sys
import time
import logging
import re
from bson.objectid import ObjectId
from flask import Flask, request, Response, jsonify, send_file, send_from_directory
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
from utils import response_json,int_to_slug,slug_to_int
from werkzeug.contrib.fixers import ProxyFix
import pytz


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

def main(port: int) -> None:
    """Run the server programatically"""

    # This will be ``None`` if all the relevant environment variables are not defined or if
    # there is an exception when connecting to the database.
    client = MongoClient('mongodbsvc', 27017)
    db = client.pymongo_test
    app = make_app(demo_db=db)
    CORS(app)

    http_server = WSGIServer(('0.0.0.0', port), app)

    http_server.serve_forever()


def make_app(demo_db) -> Flask:
    app = Flask(__name__)  # pylint: disable=invalid-name
    start_time = datetime.now(pytz.utc)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    app.predictors = {}
    app.max_request_lengths = {} # requests longer than these will be rejected to prevent OOME
    app.wsgi_app = ProxyFix(app.wsgi_app) # sets the requester IP with the X-Forwarded-For header



    @app.errorhandler(ServerError)
    def handle_invalid_usage(error: ServerError) -> Response:  # pylint: disable=unused-variable
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

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
        logging.info('This is an info message')
        if request.method == "OPTIONS":
            return Response(response="", status=200)
        
        data = request.get_json()
   
        model = model_name.lower()

        output=response_json(data,model)

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
        posts.update_one(myquery, newvalues)
        return json.dumps(output).encode('utf8')



        return jsonify(output)

    return app

if __name__ == "__main__":

    print("app is running")
    main(port=8003)
