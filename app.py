from flask import Flask, request, render_template, jsonify
from flask_restful import Api
from resources.news import NewsList, AddNews, Home
from db import db

import json
import os

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'kavida-test',
    'host': 'mongodb+srv://admin:bCzsuWTHxrUuahkK@cluster0.qrnjb.mongodb.net/kavida-test?retryWrites=true&w=majority',
    'port': 27017
}


db.init_app(app)

api = Api(app)

api.add_resource(Home, '/')
api.add_resource(NewsList, '/overview/news')
api.add_resource(AddNews, '/overview/news')
