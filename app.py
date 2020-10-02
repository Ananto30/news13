from flask import Flask, jsonify, render_template
from flask_caching import Cache
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_sslify import SSLify

from prothom_alo_bangladesh import get_bangladesh_news
from prothom_alo_feed import get_all_news

app = Flask(__name__, static_folder="static", static_url_path="")

sslify = SSLify(app)

cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route("/")
@cache.cached(timeout=300)
def all_news():
    news_list = get_all_news()
    return render_template("news.html", news_list=news_list)


@app.route("/bangladesh")
@cache.cached(timeout=300)
def bangladesh_news():
    news_list = get_bangladesh_news()
    return render_template("news.html", news_list=news_list)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
