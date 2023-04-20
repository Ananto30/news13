from datetime import datetime, timedelta
from pprint import pprint

from dateutil import parser
from pymongo import MongoClient

from scripts.helpers import pretty_date, print_headlines
from scripts.models import News

BANGLADESH_NEWS_CATEGORIES = [
    "রাজধানী",
    "জেলা",
    "করোনাভাইরাস",
    "অপরাধ",
    "পরিবেশ",
    "bangladesh",
]


class NewsStore:
    """
    MongoDB store for news
    """

    DB_NAME = "news"
    COLLECTION_NAME = "prothomalo"

    def __init__(self, mongo_uri) -> None:
        client: MongoClient = MongoClient(mongo_uri)
        self.database = client[NewsStore.DB_NAME]
        self.collection = self.database[NewsStore.COLLECTION_NAME]

    def collect_latest_news(self, news_list: list[News]):
        db_news = [
            News(**n)
            for n in list(
                self.collection.aggregate(
                    [
                        {"$sort": {"published_time": -1}},
                        {"$limit": 5},
                    ]
                )
            )
        ]

        last_db_news_timestamp = (
            max([n.published_time.timestamp() for n in db_news]) if db_news else 0
        )

        latest_news = [
            news
            for news in news_list
            if news.published_time.timestamp() > last_db_news_timestamp
        ]
        if latest_news:
            self.collection.insert_many([news.dict() for news in latest_news])
            print_headlines(latest_news)

    def get_news(self, offset, limit):
        limit = 20 if limit > 20 else limit
        pipeline = [
            {"$sort": {"published_time": -1}},
            {"$skip": offset},
            {"$limit": limit},
        ]
        news_list = list(self.collection.aggregate(pipeline))
        for news in news_list:
            news["time_ago"] = pretty_date(parser.parse(news["published_time"]))
        return news_list

    def get_bangladesh_news(self, offset, limit):
        limit = 20 if limit > 20 else limit
        news_list = list(
            self.collection.find({"category": {"$in": BANGLADESH_NEWS_CATEGORIES}})
            .sort("published_time", -1)
            .skip(offset)
            .limit(limit)
        )
        for news in news_list:
            news["time_ago"] = pretty_date(parser.parse(news["published_time"]))
        return news_list

    def get_duplicate_news(self):
        duplicate_news = list(
            self.collection.aggregate(
                [
                    {"$group": {"_id": "$link", "count": {"$sum": 1}}},
                    {"$match": {"_id": {"$ne": None}, "count": {"$gt": 1}}},
                    {"$project": {"link": "$_id", "_id": 0}},
                ]
            )
        )
        for news in duplicate_news:
            duplicates = list(self.collection.find({"link": news["link"]}))
            pprint(duplicates)

            # should_remove = duplicates[1:]
            # for news in should_remove:
            #     self.collection.delete_one({"_id": news["_id"]})

    def delete_news_older_than(self, days) -> int:
        return self.collection.delete_many(
            {
                "published_time": {
                    "$lt": (datetime.utcnow() - timedelta(days=days)).isoformat()
                }
            }
        ).deleted_count

    def get_distinct_categories(self):
        news = list(self.collection.distinct("category"))
        pprint(news)
