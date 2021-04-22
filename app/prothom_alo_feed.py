import requests as rq
from bs4 import BeautifulSoup


def get_all_news():
    page = rq.get("https://prod-qt-images.s3.amazonaws.com/production/prothomalo-bangla/feed.xml")

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
        category = i.find("category")
        category = category['term']
        a_news = {
            "source": "prothom_alo",
            "title": title,
            "summary": summary,
            "author": author,
            "published_time": time,
            # "time_ago": pretty_date(dateutil.parser.parse(time)),
            "link": link["href"],
            "category": category,
        }

        news.append(a_news)
        # print(title)

    return news

# pprint(get_all_news())
