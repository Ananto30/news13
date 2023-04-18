"""
Collect news from Prothom Alo and store in MongoDB
"""

import os
from pprint import pprint

from scripts.news_store import NewsStore
from scripts.prothom_alo_feed import get_all_news

news_store = NewsStore(os.getenv("MONGO_URI"))


if __name__ == "__main__":
    all_news = get_all_news()
    pprint(all_news)
    news_store.collect_latest_news(all_news)
