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



# class FinancialNews(db.Document):
#     title = db.StringField()

# @app.route('/')
# def home():
#     return jsonify({'result': "Kavida Test APIs"})
#
#
# @app.route('/overview/news', methods=['GET', 'POST'])
# def news_controller():
#     if request.method == 'GET':
#         data = {"message": "in a GET method"}
#         return jsonify(data), 200
#
#         # students = table.scan()['Items']
#         # return json_response(students)
#     else:
#         try:
#             # record = json.loads(request.data)
#             record = request.get_json(force=True)
#
#             news = FinancialNews(title=record['title'])
#             news.save()
#             return jsonify(news), 200
#             # _json = request.get_json(force=True)
#             # _title = _json['title']
#             # _timestamp = _json['timestamp']
#             # _reliability = _json['reliability']
#             # _severity = _json['severity']
#             # _summary = _json['summary']
#             # _newsLink = _json['newsLink']
#             # _categories = _json['categories']
#             # # validate the received values
#             # if _title and _timestamp and _reliability and _severity and _summary and _newsLink and _categories:
#             #     # save in
#             #     _hashed_password = generate_password_hash(_password)
#             #     # save details
#             #     input = {"title": _title,
#             #              "timestamp": _timestamp,
#             #              "reliability": _reliability,
#             #              "severity": _severity,
#             #              "summary": _summary,
#             #              "newsLink": _newsLink,
#             #              "categories": _categories
#             #              }
#             #     id = mongo.db.financial_news.insert(input)
#             #
#             #     return jsonify({"message": "News Added Successfully", "status": id}), 200
#             # else:
#             #     return not_found()
#         except:
#             return jsonify({"message": "News Added Not Successfully", "status": "false"}), 200
