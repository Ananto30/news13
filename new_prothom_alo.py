import json
from collections import OrderedDict
from datetime import datetime
from pprint import pprint

import requests as rq
from bs4 import BeautifulSoup
from pymongo import MongoClient

import dateutil.parser
import pytz

# client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
# db = client.news
# news = db.news

# news.delete_many({"source": "prothom_alo"})

page = rq.get("https://www.prothomalo.com/bangladesh/article?page=1")

soup = BeautifulSoup(page.content, "html.parser")

info = soup.find_all("div", class_="col col1")


def get_news():

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
        # a_news = [
        #     ('source','prothom_alo'),
        #     ('title',title),
        #     ('summary',summary),
        #     ('author',author),
        #     ('published_time',time),
        #     ('link',link)
        # ]
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
        print(time)

    return news


# pprint(news)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now(pytz.utc)
    print(time)
    print(now)
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "এই মাত্র"
        if second_diff < 60:
            return bangla_number(str(round(second_diff))) + " সেকেন্ড আগে"
        if second_diff < 120:
            return "১ মিনিট আগে"
        if second_diff < 3600:
            return bangla_number(str(round(second_diff / 60))) + " মিনিট আগে"
        if second_diff < 7200:
            return "১ ঘন্টা আগে"
        if second_diff < 86400:
            return bangla_number(str(round(second_diff / 3600))) + " ঘন্টা আগে"
    if day_diff == 1:
        return "গতকাল"
    if day_diff < 7:
        return bangla_number(str(round(day_diff))) + " দিন আগে"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def bangla_number(string):
    number_map = {
        "0": "০",
        "1": "১",
        "2": "২",
        "3": "৩",
        "4": "৪",
        "5": "৫",
        "6": "৬",
        "7": "৭",
        "8": "৮",
        "9": "৯",
    }

    return "".join([number_map[s] for s in string])
