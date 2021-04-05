import dateutil.parser
from pymongo import MongoClient


class NewsStore:
    DB_NAME = "news"
    COLLECTION_NAME = "prothomalo"

    def __init__(self, mongo_uri) -> None:
        client = MongoClient(mongo_uri)
        self.db = client[NewsStore.DB_NAME]
        self.cursor = self.db[NewsStore.COLLECTION_NAME]

    def store_news(self, news):
        pipeline = [{"$sort": {"published_time": -1}}, {"$limit": 1}]
        db_news = list(self.cursor.aggregate(pipeline))
        last_db_news_time = dateutil.parser.parse(db_news[0]["published_time"])
        latest_news = []
        for n in news:
            news_time = dateutil.parser.parse(n["published_time"])
            if news_time > last_db_news_time:
                latest_news.append(n)
        self.cursor.insert_many(latest_news)

    def get_news(self, offset, limit):
        limit = 20 if limit > 20 else limit
        pipeline = [
            {"$sort": {"published_time": -1}},
            {"$skip": offset},
            {"$limit": limit},
        ]
        return list(self.cursor.aggregate(pipeline))
