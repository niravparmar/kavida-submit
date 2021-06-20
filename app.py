from flask import Flask, request, render_template, jsonify
from flask_restful import Api
from resources.news import NewsList, AddNews, Home
from db import db

import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://FhdmxLFTg0:ix9ywg7HMe@remotemysql.com:3306/FhdmxLFTg0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Home, '/')
api.add_resource(NewsList, '/overview/news')
api.add_resource(AddNews, '/overview/news')

# app.run(port=5000, debug=True)
