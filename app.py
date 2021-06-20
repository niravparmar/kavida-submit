from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
import json
import datetime
import math
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://FhdmxLFTg0:ix9ywg7HMe@remotemysql.com:3306/FhdmxLFTg0'
db = SQLAlchemy(app)


# Model
class News(db.Model):
    __tablename__ = 'news_table'

    news_table_id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    timestamp = db.Column(db.Integer(), nullable=True)
    reliability = db.Column(db.Integer(), nullable=True)
    severity = db.Column(db.Integer(), nullable=True)
    summary = db.Column(db.String(500), nullable=True)
    newsLink = db.Column(db.String(500), nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, timestamp, reliability, severity, summary, newsLink):
        self.title = title
        self.timestamp = timestamp
        self.reliability = reliability
        self.severity = severity
        self.summary = summary
        self.newsLink = newsLink

    def __repr__(self):
        return f"{self.news_table_id}"


class Category(db.Model):
    __tablename__ = 'category_table'

    category_id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(300), nullable=True)
    news_table_id = db.Column(db.Integer(), nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, category_name, news_table_id):
        self.category_name = category_name
        self.news_table_id = news_table_id

    def __repr__(self):
        return f"{self.category_id}"


db.create_all()


class NewsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = News
        sqla_session = db.session

    news_table_id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    timestamp = fields.Number(required=True)
    reliability = fields.Number(required=True)
    severity = fields.Number(required=True)
    summary = fields.String(required=True)
    newsLink = fields.String(required=True)


class CategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session

    category_id = fields.Number(dump_only=True)
    category_name = fields.String(required=True)
    news_table_id = fields.Number(required=True)


@app.route("/overview/news", methods=['POST', 'GET'])
def NewsApi():
    if request.method == "POST":
        data = request.get_json()
        category = data['categories']

        try:
            if (len(data['categories']) <= 3) and data['title'] and data['timestamp'] and data['reliability'] and data[
                'severity'] and data['summary'] and data['newsLink']:
                del data['categories']

                news_schema = NewsSchema()
                news = news_schema.load(data)
                result = news_schema.dump(news.create())
                result_id = result['news_table_id']

                for x in category:
                    category_schema = CategorySchema()
                    category_input = {
                        "category_name": x,
                        "news_table_id": result_id
                    }
                    category_record = category_schema.load(category_input)
                    category_result = category_schema.dump(category_record.create())

                return jsonify({
                    "meta": {
                        "statusCode": 20,
                        "messageClient": "string",
                        "messageServer": "string",
                        "errorDetail": "string"
                    },
                    "data": True,
                    "pagination": {
                        "totalData": 0,
                        "totalPage": 0
                    }
                }), 200
            else:
                return jsonify({
                    "meta": {
                        "statusCode": 42,
                        "messageClient": "Validation error",
                        "messageServer": "string",
                        "errorDetail": "string"
                    }, "data": {},
                    "pagination": {}
                }), 400

        except:
            return jsonify({
                "meta": {
                    "statusCode": 42,
                    "messageClient": "Validation error",
                    "messageServer": "string",
                    "errorDetail": "string"
                }, "data": {},
                "pagination": {}
            }), 400

    else:
        try:
            data = {
                "page": request.args.get('page'),
                "limit": request.args.get('limit'),
                "date": request.args.get('date'),
                "severity": request.args.get('severity'),
                "supplier": request.args.get('supplier')
            }

            if data['page'] and data['limit']:
                # date timestamp getter
                today = datetime.datetime.now()
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                week = datetime.datetime.now() - datetime.timedelta(days=7)
                month = datetime.datetime.now() - datetime.timedelta(days=30)

                def timestamp_getter(argument):
                    switcher = {
                        1: datetime.datetime.strptime(today.strftime("%d/%m/%Y"), "%d/%m/%Y").timestamp(),
                        2: datetime.datetime.strptime(yesterday.strftime("%d/%m/%Y"), "%d/%m/%Y").timestamp(),
                        3: datetime.datetime.strptime(week.strftime("%d/%m/%Y"), "%d/%m/%Y").timestamp(),
                        4: datetime.datetime.strptime(month.strftime("%d/%m/%Y"), "%d/%m/%Y").timestamp(),
                    }
                    return switcher.get(argument, 0)

                def severity_getter(argument):
                    switcher = {
                        1: [80, 100],
                        2: [50, 79],
                        3: [0, 49]
                    }
                    return switcher.get(argument, [0, 100])

                timestampfinal = timestamp_getter(int(data["date"]))
                severityfinal = severity_getter(int(data["severity"]))

                result = News.query.filter(
                    News.timestamp >= timestampfinal,
                    News.severity >= severityfinal[0],
                    News.severity <= severityfinal[1],
                )

                news_schema = NewsSchema(many=True)
                news_list = news_schema.dump(result)
                totaldata = len(news_list)
                totalpage = math.ceil(totaldata / int(data['limit']))

                return jsonify({
                    "meta": {
                        "statusCode": 20,
                        "messageClient": "string",
                        "messageServer": "string",
                        "errorDetail": "string"
                    },
                    "data": news_list,
                    "pagination": {
                        "totalData": totaldata,
                        "totalPage": totalpage
                    }
                }), 200

            else:
                raise ValueError()
        except:
            return jsonify({
                "meta": {
                    "statusCode": 42,
                    "messageClient": "Validation error",
                    "messageServer": "string",
                    "errorDetail": "string"
                }, "data": {},
                "pagination": {}
            }), 400
