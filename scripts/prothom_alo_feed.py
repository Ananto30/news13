import requests
from bs4 import BeautifulSoup

from scripts.models import News


def get_latest_news() -> list[News]:
    """
    Gather all news from Prothom Alo
    """

    page = requests.get(
        "https://prod-qt-images.s3.amazonaws.com/production/prothomalo-bangla/feed.xml",
        timeout=30,
    )

    soup = BeautifulSoup(page.content, "lxml-xml")
    entries = soup.find_all("entry")

    news_list = []
    for entry in entries:
        news = _parse_news(entry)
        if news:
            news_list.append(news)

    return news_list


def _parse_news(element):
    title = element.find("title").get_text()
    summary = BeautifulSoup(element.find("summary").get_text().strip(), "html.parser")
    if summary:
        summary = summary.get_text().strip()
    else:
        return None
    author = element.find("author").find("name").get_text()
    time = element.find("published").get_text()
    link = element.find("link")["href"]
    category = element.find("category")["term"]
    return News(
        source="prothom_alo",
        title=title,
        summary=summary,
        author=author,
        published_time=time,
        link=link,
        category=category,
    )
