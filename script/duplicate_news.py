import os

from app.news_store import NewsStore

news_store = NewsStore(os.getenv("MONGO_URI"))
news_store.get_duplicate_news()
