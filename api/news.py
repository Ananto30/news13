import sys
from datetime import datetime

import dateutil.parser
import pytz
import requests as rq
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
from flask_caching import Cache

sys.path.append("..")
from prothom_alo_feed import get_all_news
from prothom_alo_bangladesh import get_bangladesh_news


app = Flask(__name__, static_folder="static", static_url_path="")


cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route("/api/news")
@cache.cached(timeout=30)
def all_news():
    news_list = get_all_news()
    # return render_template("news.html", news_list=news_list)
    return jsonify(news_list), 200


@app.route("/api/news/bangladesh")
@cache.cached(timeout=30)
def bangladesh_news():
    news_list = get_bangladesh_news()
    # return render_template("news.html", news_list=news_list)
    return jsonify(news_list), 200
