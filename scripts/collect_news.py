"""
Collect news from Prothom Alo and store in MongoDB
"""

import os

from scripts.helpers import print_headlines
from scripts.news_store import NewsStore
from scripts.prothom_alo_feed import get_latest_news

news_store = NewsStore(os.getenv("MONGO_URI"))


if __name__ == "__main__":
    latest_news = get_latest_news()
    print_headlines(latest_news)
    news_store.collect_latest_news(latest_news)
