import dateutil.parser
import requests as rq
from bs4 import BeautifulSoup

from scripts.helpers import pretty_date


def get_bangladesh_news():
    page = rq.get("https://www.prothomalo.com/bangladesh")

    soup = BeautifulSoup(page.content, "html.parser")

    info = soup.find_all("div", class_="bn-story-card")

    news = []

    for i in info:
        title = i.find("h2", class_="headline")
        title = title.get_text()
        summary = i.find("span")
        if summary:
            summary = summary.get_text().strip()
        else:
            continue
        author = i.find("span", class_="author aitm")
        if author:
            author = author.get_text()
        time = i.find("time", class_="published-time")
        if time:
            time = time["data-published"]
        link = i.find("a")
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

        news.append(a_news)
        # print(title)

    return news


# pprint(get_bangladesh_news())
