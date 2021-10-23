import os
from pprint import pprint

from app.news_store import NewsStore
from app.prothom_alo_feed import get_all_news

news_store = NewsStore(os.getenv("MONGO_URI"))
all_news = get_all_news()
pprint(all_news)
news_store.collect_latest_news(all_news)
