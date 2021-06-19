from flask_restful import Resource, reqparse
from models.news import News
import json
import datetime
import math


class Home(Resource):

    def get(self):
        try:
            return {'message': "Welcome to Kavida-Demo APIs"}, 200
        except:
            return {'message': 'Error from server side'}, 500

class NewsList(Resource):

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('page', type=int, location='args')
        parser.add_argument('limit', type=int, location='args')
        parser.add_argument('date', type=int, location='args')
        parser.add_argument('severity', type=int, location='args')
        parser.add_argument('supplier', type=str, location='args')
        try:
            data = parser.parse_args()
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

                timestampfinal = timestamp_getter(data["date"])
                severityfinal = severity_getter(data["severity"])

                response = News.objects(timestamp__gte=timestampfinal,
                                        severity__gte=severityfinal[0],
                                        severity__lte=severityfinal[1],
                                        ).to_json()

                finaloutput = json.loads(response)

                return {
                    "meta": {
                        "statusCode": 20,
                        "messageClient": "string",
                        "messageServer": "string",
                        "errorDetail": "string"
                    },
                    "data": finaloutput,
                    "pagination": {
                        "totalData": len(finaloutput),
                        "totalPage": math.ceil((len(finaloutput))/(data['limit']))
                    }
                }, 200
            else:
                return {
                       "meta": {
                           "statusCode": 42,
                           "messageClient": "Validation error",
                           "messageServer": "string",
                           "errorDetail": "string"
                       }, "data": {},
                       "pagination": {}
                   }, 400
        except:
            return {
                       "meta": {
                           "statusCode": 42,
                           "messageClient": "Validation error",
                           "messageServer": "string",
                           "errorDetail": "string"
                       }, "data": {},
                       "pagination": {}
                   }, 400


class AddNews(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title', type=str)
    parser.add_argument('timestamp', type=int)
    parser.add_argument('reliability', type=int, )
    parser.add_argument('severity', type=int)
    parser.add_argument('summary', type=str)
    parser.add_argument('newsLink', type=str)
    parser.add_argument('categories', type=str, action='append')

    def post(self):
        data = AddNews.parser.parse_args()

        if len(data['categories']) <= 3 and data['title'] and data['timestamp'] and data['reliability'] and data[
            'severity'] and data['summary'] and data['newsLink']:

            try:
                News(**data).save()
                return {
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
                       }, 200

            except:
                return {
                       "meta": {
                           "statusCode": 42,
                           "messageClient": "Validation error",
                           "messageServer": "string",
                           "errorDetail": "string"
                       }, "data": {},
                       "pagination": {}
                   }, 400

        else:
            return {
                       "meta": {
                           "statusCode": 42,
                           "messageClient": "Validation error",
                           "messageServer": "string",
                           "errorDetail": "string"
                       }, "data": {},
                       "pagination": {}
                   }, 400
