import dateutil.parser
import requests as rq
from bs4 import BeautifulSoup
from pprint import pprint


from app.helpers import pretty_date


def get_all_news():

    page = rq.get("https://www.prothomalo.com/feed")

    soup = BeautifulSoup(page.content, "lxml-xml")

    info = soup.find_all("entry")

    news = []

    for i in info:
        title = i.find("title")
        title = title.get_text()
        content = i.find("summary")
        summary = BeautifulSoup(content.get_text().strip(), "html.parser")
        if summary:
            summary = summary.get_text().strip()
            # summary = summary[:-10]
        else:
            continue
        author = i.find("author")
        author = author.find("name")
        if author:
            author = author.get_text()
        time = i.find("published")
        if time:
            time = time.get_text()
        link = i.find("link")
        a_news = {
            "source": "prothom_alo",
            "title": title,
            "summary": summary,
            "author": author,
            "published_time": time,
            "time_ago": pretty_date(dateutil.parser.parse(time)),
            "link": link["href"],
        }

        news.append(a_news)
        # print(title)

    return news


# pprint(get_all_news())
