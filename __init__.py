# -*- coding: utf-8 -*-
import json
import requests
from datetime import datetime
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from bson import json_util
from flask import Flask, render_template, Response, request, jsonify
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import xmltodict
import _configs as cfg
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
update_on_launch = False


# #############################################################
#     # DB_INFO
# #############################################################

# client = MongoClient(cfg.mongo_uri, maxPoolSize=50, wtimeout=2000)
# db = client['ddbb']  # database
# collection = db['main_collection']  # collection


#############################################################
    # Scheduler routine
#############################################################

# scheduler = BackgroundScheduler()
# scheduler.start()


#############################################################
    # Services/DB methods
#############################################################

# def get_page(kwargs):
#     pass


#############################################################
    # Http API
#############################################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/noticias')
def noticias():
    return render_template('noticias.html')


@app.route('/gettest')
def get_test():
    return Response(
        json_util.dumps({
            "result": "Ok"
        }),
        mimetype='application/json'
    )


@app.route('/posttest', methods=['POST'])
def post_test():
    return Response(
        json_util.dumps({
            "result": "Ok",
            "echo": request.json,
            "mimetype": request.mimetype
        }),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     app.run(ssl_context = 'adhoc')

