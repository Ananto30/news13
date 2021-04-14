import json
import os
import textwrap

from bson import ObjectId
from flask import Flask, request, Response, send_from_directory
from flask_caching import Cache
from flask_cors import CORS

from app.news_store import NewsStore
from app.prothom_alo_feed import get_all_news

app = Flask(__name__, static_folder="../web-app/public", static_url_path="/")

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


@cache.cached(timeout=300)
def cache_wrapper():
    return get_all_news()


@cache.cached(timeout=300)
def cached_all_news(page):
    offset, limit = calculate_offset_limit(page)
    data = {"news": news_store.get_news(offset, limit), "page": page}
    return data


@cache.cached(timeout=300)
def cached_bangladesh_news(page):
    offset, limit = calculate_offset_limit(page)
    data = {"news": news_store.get_bangladesh_news(offset, limit), "page": page}
    return data


@app.route("/api/news/bangladesh/<page>")
def bangladesh_news_api(page):
    return JSONEncoder().encode(cached_bangladesh_news(page))


@app.route("/api/news/all/<page>")
def news_api(page):
    return JSONEncoder().encode(cached_all_news(page))


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    user_agent = request.headers.get("User-Agent")
    data = cached_all_news(1)
    if is_plaintext_client(user_agent):
        resp = ""
        for news in data["news"]:
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

    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
