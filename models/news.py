from db import db

class News(db.Model):

    __tablename__ = 'news'

    newsid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000))
    timestamp = db.Column(db.Integer())
    reliability = db.Column(db.Integer())
    severity = db.Column(db.Integer())
    summary = db.Column(db.String(500))
    newsLink = db.Column(db.String(300))
    categories = db.Column(db.String(100))

    def __init__(self, title, timestamp, reliability, severity, summary, newsLink, categories):
        self.title = title
        self.timestamp = timestamp
        self.reliability = reliability
        self.severity = severity
        self.summary = summary
        self.newsLink = newsLink
        self.categories = categories

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_news(self):
        news_list = []
        for news in db.session.query(News).all():
            news_list.append({'title': news.title, 'timestamp': news.timestamp, 'reliability': news.reliability, 'severity': news.severity, 'summary': news.summary, 'newsLink': news.newsLink, 'categories': news.categories})
        return news_list

    def get_news_by_filter(self, timestampfinal, severityfinal):
        news_list = []
        try:
            for news in db.session.query(News).filter(
                    News.timestamp >= timestampfinal, News.severity >= int(severityfinal[0]), News.severity <= int(severityfinal[1])
                                                     ):
                news_list.append({'title': news.title, 'timestamp': news.timestamp, 'reliability': news.reliability, 'severity': news.severity, 'summary': news.summary, 'newsLink': news.newsLink, 'categories': news.categories})
            return news_list
        except Exception as ex:
            print(ex.args)
