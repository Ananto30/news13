from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from pymongo import MongoClient
import datetime

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

client = MongoClient("mongodb://ananto:hoga123@ds021346.mlab.com:21346/news")
db = client.news
news = db.news


def get_news_by_source(source):
    has_news = news.find({"source": source}, {"_id":0}).limit(10)
    if has_news:
        return has_news


def mongodb_model(data):
    d = {
        'source': data['source'],
        'title': data['title'],
        'summary': data['summary'],
        'author': data['author'],
        'published_time': data['published_time'],
        'link': data['link']
    }
    return d


subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")


class NewsCollection(Resource):
    def get(self):
        cursor = news.find({},{"_id":0}).limit(10)
        all_data = []
        for data in cursor:
            all_data.append(data)
        return all_data

        # def post(self):
        #     args = subscriber_request_parser.parse_args()
        #     users.append(args)
        #     return {"msg": "Subscriber added", "subscriber_data": args}


class News(Resource):
    def get(self, source):
        cursor = get_news_by_source(source)
        if not cursor:
            return {"error": "Source not found"}
        all_data = []
        for data in cursor:
            all_data.append(data)
        return all_data

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


api.add_resource(NewsCollection, '/news')
api.add_resource(News, '/news/<source>')

if __name__ == '__main__':
    app.run()
