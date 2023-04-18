import os

from scripts.news_store import NewsStore

news_store = NewsStore(os.getenv("MONGO_URI"))


if __name__ == "__main__":
    count = news_store.delete_news_older_than(365)
    print(f"Deleted {count} old news")
