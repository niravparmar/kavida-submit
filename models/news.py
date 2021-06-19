from db import db


class News(db.Document):

    __tablename__ = 'news'

    title = db.StringField()
    timestamp = db.IntField()
    reliability = db.IntField()
    severity = db.IntField()
    summary = db.StringField()
    newsLink = db.StringField()
    categories = db.ListField()
