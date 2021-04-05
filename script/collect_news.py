import os

from app.news_store import NewsStore
from app.prothom_alo_feed import get_all_news

news_store = NewsStore(os.getenv("MONGO_URI"))
news_store.collect_latest_news(get_all_news())
