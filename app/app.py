from flask import Flask, render_template, request, Response
from flask_caching import Cache

from app.prothom_alo_bangladesh import get_bangladesh_news
from app.prothom_alo_feed import get_all_news
from pprint import pprint
import textwrap

app = Flask(__name__, static_folder="static", static_url_path="")


cache = Cache(app, config={"CACHE_TYPE": "simple"})


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@cache.cached(timeout=300)
def cache_wrapper():
    return get_all_news()


@app.route("/")
def all_news():
    user_agent = request.headers.get("User-Agent")

    news_list = cache_wrapper()

    if is_plaintext_client(user_agent):
        resp = ""
        for news in news_list:
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

    return render_template("news.html", news_list=news_list)


@app.route("/bangladesh")
@cache.cached(timeout=300)
def bangladesh_news():
    news_list = get_bangladesh_news()
    return render_template("news.html", news_list=news_list)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
