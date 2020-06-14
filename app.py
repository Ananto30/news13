from flask import Flask, jsonify, render_template
from flask_caching import Cache
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_sslify import SSLify

from prothom_alo_bangladesh import get_bangladesh_news
from prothom_alo_feed import get_all_news

app = Flask(__name__, static_folder="static", static_url_path="")

sslify = SSLify(app)

api = Api(app, prefix="/api/v1")

cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
# db = client.news
# news = db.news


def get_news_by_source(source):
    has_news = news.find({"source": source}, {"_id": 0}).limit(10)
    if has_news:
        return has_news


def mongodb_model(data):
    d = {
        "source": data["source"],
        "title": data["title"],
        "summary": data["summary"],
        "author": data["author"],
        "published_time": data["published_time"],
        "link": data["link"],
    }
    return d


subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument(
    "name", type=str, required=True, help="Name has to be valid string"
)
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument(
    "id", type=int, required=True, help="Please enter valid integer as ID"
)


class NewsCollection(Resource):
    def get(self):
        cursor = news.find({}, {"_id": 0}).limit(10)
        all_data = []
        for data in cursor:
            all_data.append(data)
        return jsonify(all_data)

        # def post(self):
        #     args = subscriber_request_parser.parse_args()
        #     users.append(args)
        #     return {"msg": "Subscriber added", "subscriber_data": args}


class News(Resource):
    def get(self, source):
        cursor = get_news_by_source(source)
        if not cursor:
            return jsonify({"error": "Source not found"})
        all_data = []
        for data in cursor:
            all_data.append(data)
        return jsonify(all_data)

        # def put(self, id):
        #     args = subscriber_request_parser.parse_args()
        #     user = get_user_by_id(id)
        #     if user:
        #         users.remove(user)
        #         users.append(args)
        #
        #     return args
        #
        # def delete(self, id):
        #     user = get_user_by_id(id)
        #     if user:
        #         users.remove(user)
        #
        #     return {"message": "Deleted"}


api.add_resource(NewsCollection, "/news")
api.add_resource(News, "/news/<source>")


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
