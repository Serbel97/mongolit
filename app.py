import os

from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_pymongo import pymongo

BASE_DIR = Path(__file__).resolve(strict=True).parent
ENV_FILE = os.path.join(BASE_DIR, '.env')

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE, verbose=True)
else:
    exit(0)

client = pymongo.MongoClient(os.getenv('MONGODB'))
db = client.get_database('blog')
article_collection = pymongo.collection.Collection(db, 'articles')


class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        pass

    @staticmethod
    def _get_item(_id):
        return db.articles.find_one({'_id': _id})

    def get(self, _id: int):
        article = self._get_item(_id)
        return render_template("index.html", article=article)

    def put(self, id):
        item = self._get_item(id)
        return jsonify(item.to_json())

    def delete(self, id):
        return "", 204


def register_api(app, model, name):
    item = ItemAPI.as_view(f"{name}-item", model)
    app.add_url_rule(f"/{name}/<int:_id>", view_func=item)


flask = Flask(__name__)

if __name__ == '__main__':
    flask.run()


register_api(flask, ItemAPI, "users")
