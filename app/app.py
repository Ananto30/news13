import json
import os
import textwrap

from bson import ObjectId
from flask import Flask, render_template, request, Response
from flask_caching import Cache
from flask_cors import CORS

from app.news_store import NewsStore
from app.prothom_alo_bangladesh import get_bangladesh_news
from app.prothom_alo_feed import get_all_news

app = Flask(__name__, static_folder="static", static_url_path="")

cache = Cache(app, config={"CACHE_TYPE": "simple"})

cors = CORS(app, resources={r"/*": {"origins": "*"}})
news_store = NewsStore(os.getenv("MONGO_URI"))

PAGE_SIZE = 20


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def is_plaintext_client(user_agent):
    plaintext_clients = [
        "curl",
        "wget",
        "fetch",
        "httpie",
        "lwp-request",
        "openbsd ftp",
        "python-requests",
    ]
    return any([x in user_agent for x in plaintext_clients])


def calculate_offset_limit(page):
    page = int(page)
    offset = (page - 1) * PAGE_SIZE
    limit = page * PAGE_SIZE
    return offset, limit


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@cache.cached(timeout=300)
def cache_wrapper():
    return get_all_news()


@cache.cached(timeout=300)
def cache_db_wrapper(page):
    offset, limit = calculate_offset_limit(page)
    data = {'news': news_store.get_news(offset, limit), 'page': page}
    return data


@app.route("/")
def all_news():
    user_agent = request.headers.get("User-Agent")

    data = cache_db_wrapper(1)

    if is_plaintext_client(user_agent):
        resp = ""
        for news in data.news:
            resp += (
                    textwrap.fill(news.get("title"), 100)
                    + "\n"
                    + "-" * len(news.get("title"))
                    + "\n"
                    + textwrap.fill(news.get("summary"), 100)
                    + "\n"
                    + "-" * 80
                    + "\n"
                    + textwrap.fill(news.get("link"), 100)
                    + "\n"
                    + "=" * 95
                    + "\n"
            )
        return Response(resp.encode("utf-8"), mimetype="text/plain")

    return render_template("news.html", data=data)


@app.route("/api/news/<page>")
def news_api(page):
    return JSONEncoder().encode(cache_db_wrapper(page))


@app.route("/bangladesh")
@cache.cached(timeout=300)
def bangladesh_news():
    news_list = get_bangladesh_news()
    return render_template("news.html", data={'news': news_list})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
