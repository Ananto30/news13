import requests
from bs4 import BeautifulSoup


def get_all_news():
    """
    Gather all news from Prothom Alo
    """

    page = requests.get(
        "https://prod-qt-images.s3.amazonaws.com/production/prothomalo-bangla/feed.xml",
        timeout=30,
    )

    soup = BeautifulSoup(page.content, "lxml-xml")
    entries = soup.find_all("entry")

    news = []

    for entry in entries:
        title = entry.find("title")
        title = title.get_text()
        content = entry.find("summary")
        summary = BeautifulSoup(content.get_text().strip(), "html.parser")
        if summary:
            summary = summary.get_text().strip()
            # summary = summary[:-10]
        else:
            continue
        author = entry.find("author")
        author = author.find("name")
        if author:
            author = author.get_text()
        time = entry.find("published")
        if time:
            time = time.get_text()
        link = entry.find("link")
        category = entry.find("category")
        category = category["term"]
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

    return news
