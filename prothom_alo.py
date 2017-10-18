import requests as rq
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from collections import OrderedDict
import json

client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
db = client.news
news = db.news

news.delete_many({"source": "prothom_alo"})

page = rq.get('http://www.prothom-alo.com/archive')

soup = BeautifulSoup(page.content, 'html.parser')

info = soup.find_all('div', class_='col col1')

for i in info:
    title = i.find('span', class_='title')
    title = title.get_text()
    summary = i.find('div', class_='summery')
    summary = summary.get_text().strip()
    author = i.find('span', class_='author aitm')
    if author:
        author = author.get_text()
    time = i.find('span', class_='time aitm')
    time = time['data-published']
    link = i.find('a', class_='link_overlay')
    link = 'prothom-alo.com/'+link['href']
    # a_news = [
    #     ('source','prothom_alo'),
    #     ('title',title),
    #     ('summary',summary),
    #     ('author',author),
    #     ('published_time',time),
    #     ('link',link)
    # ]
    a_news = {
        'source':'prothom_alo',
        'title':title,
        'summary':summary,
        'author':author,
        'published_time':time,
        'link':link
    }
    news.insert_one(a_news)
    print('inserted')