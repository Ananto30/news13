"""
Collect news from Prothom Alo and store in MongoDB
"""

import os

from scripts.news_store import NewsStore
from scripts.prothom_alo_feed import get_latest_news

news_store = NewsStore(os.getenv("MONGO_URI"))


if __name__ == "__main__":
    latest_news = get_latest_news()
    news_store.collect_latest_news(latest_news)
    total_archived_news = news_store.total_news()
    print(f"Total archived news: {total_archived_news}")
