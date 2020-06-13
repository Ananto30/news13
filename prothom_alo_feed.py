import dateutil.parser
import requests as rq
from bs4 import BeautifulSoup

# news.delete_many({"source": "prothom_alo"})
from helpers import pretty_date

# client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
# db = client.news
# news = db.news

page = rq.get("https://www.prothomalo.com/feed/")

soup = BeautifulSoup(page.content, "lxml-xml")

info = soup.find_all("item")


def get_all_news():
    news = []

    for i in info:
        title = i.find("title")
        title = title.get_text()
        content = i.find("content:encoded")
        summary = BeautifulSoup(content.get_text().strip(), "html.parser")
        if summary:
            summary = summary.get_text().strip()
            summary = summary[:-10]
        else:
            continue
        author = i.find("dc:creator")
        if author:
            author = author.get_text()
        time = i.find("pubDate")
        if time:
            time = time.get_text()
        link = i.find("link").get_text()
        a_news = {
            "source": "prothom_alo",
            "title": title,
            "summary": summary,
            "author": author,
            "published_time": time,
            "time_ago": pretty_date(dateutil.parser.parse(time)),
            "link": link,
        }
        # news.insert_one(a_news)
        news.append(a_news)
        print(title)

    return news

# pprint(get_news())
