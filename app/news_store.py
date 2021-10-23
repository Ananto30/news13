from datetime import datetime
from pprint import pprint

import dateutil.parser
import pytz
from pymongo import MongoClient

from app.helpers import pretty_date

BANGLADESH_NEWS_CATEGORIES = [
    "রাজধানী",
    "জেলা",
    "করোনাভাইরাস",
    "অপরাধ",
    "পরিবেশ",
    "bangladesh",
]


class NewsStore:
    DB_NAME = "news"
    COLLECTION_NAME = "prothomalo"

    def __init__(self, mongo_uri) -> None:
        client = MongoClient(mongo_uri)
        self.db = client[NewsStore.DB_NAME]
        self.cursor = self.db[NewsStore.COLLECTION_NAME]

    def collect_latest_news(self, news):
        pipeline = [{"$sort": {"published_time": -1}}, {"$limit": 5}]
        db_news = list(self.cursor.aggregate(pipeline))
        i = 0
        last_db_news_time = dateutil.parser.parse(db_news[i]["published_time"])
        while last_db_news_time > datetime.utcnow().replace(tzinfo=pytz.UTC):
            last_db_news_time = dateutil.parser.parse(db_news[i]["published_time"])
            i += 1

        latest_news = []
        for n in news:
            news_time = dateutil.parser.parse(n["published_time"])
            if news_time > last_db_news_time:
                latest_news.append(n)
        if latest_news:
            print(f"Collected news - \n{' | '.join([n['title'] for n in latest_news])}")
            self.cursor.insert_many(latest_news)

    def get_news(self, offset, limit):
        limit = 20 if limit > 20 else limit
        pipeline = [
            {"$sort": {"published_time": -1}},
            {"$skip": offset},
            {"$limit": limit},
        ]
        news_list = list(self.cursor.aggregate(pipeline))
        for news in news_list:
            news["time_ago"] = pretty_date(
                dateutil.parser.parse(news["published_time"])
            )
        return news_list

    def get_bangladesh_news(self, offset, limit):
        limit = 20 if limit > 20 else limit
        news_list = list(
            self.cursor.find({"category": {"$in": BANGLADESH_NEWS_CATEGORIES}})
                .sort("published_time", -1)
                .skip(offset)
                .limit(limit)
        )
        for news in news_list:
            news["time_ago"] = pretty_date(
                dateutil.parser.parse(news["published_time"])
            )
        return news_list

    def get_duplicate_news(self):
        duplicate_news = list(
            self.cursor.aggregate(
                [
                    {"$group": {"_id": "$link", "count": {"$sum": 1}}},
                    {"$match": {"_id": {"$ne": None}, "count": {"$gt": 1}}},
                    {"$project": {"link": "$_id", "_id": 0}},
                ]
            )
        )
        for news in duplicate_news:
            duplicates = list(self.cursor.find({"link": news["link"]}))
            pprint(duplicates)

            # should_remove = duplicates[1:]
            # for n in should_remove:
            #     self.cursor.remove({"_id": n["_id"]})

    def get_distinct_categories(self):
        news = list(self.cursor.distinct("category"))
        pprint(news)
