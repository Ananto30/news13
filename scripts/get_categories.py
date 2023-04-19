import os

from scripts.news_store import NewsStore

news_store = NewsStore(os.getenv("MONGO_URI"))


if __name__ == "__main__":
    news_store.get_distinct_categories()
