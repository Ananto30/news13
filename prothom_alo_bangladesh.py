import dateutil.parser
import requests as rq
from bs4 import BeautifulSoup

# news.delete_many({"source": "prothom_alo"})
from helpers import pretty_date

# client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
# db = client.news
# news = db.news

page = rq.get("https://www.prothomalo.com/bangladesh/article?page=1")

soup = BeautifulSoup(page.content, "html.parser")

info = soup.find_all("div", class_="col col1")


def get_bangladesh_news():
    news = []

    for i in info:
        title = i.find("span", class_="title")
        title = title.get_text()
        summary = i.find("div", class_="summery")
        if summary:
            summary = summary.get_text().strip()
        else:
            continue
        author = i.find("span", class_="author aitm")
        if author:
            author = author.get_text()
        time = i.find("span", class_="time aitm")
        if time:
            time = time["data-published"]
        link = i.find("a", class_="link_overlay")
        link = "http://www.prothom-alo.com/" + link["href"]

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

# pprint(news)
