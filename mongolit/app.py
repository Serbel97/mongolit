import json
import os
from functools import partial
from pathlib import Path

from bson import ObjectId
from dotenv import load_dotenv

from flask import Flask, render_template
from flask_pymongo import pymongo

from apps.encoders import MongoJSONEncoder
from apps.views.article import create_article, list_articles, detail_article, delete_article, update_article, \
    update_comment_article


class FlaskProject(Flask):
    def __init__(self, __name__):
        BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

        template_dir = os.path.join(BASE_DIR, 'templates')
        static_dir = os.path.join(BASE_DIR, 'static')
        super().__init__(__name__, template_folder=template_dir, static_folder=static_dir)

        ENV_FILE = os.path.join(BASE_DIR, '.env')
        if os.path.exists(ENV_FILE):
            load_dotenv(dotenv_path=ENV_FILE, verbose=True)
        else:
            exit(0)

        client = pymongo.MongoClient(os.getenv('MONGODB_KEY'))
        self.db = client.get_database(os.getenv('MONGODB'))


flask = FlaskProject(__name__)


if __name__ == '__main__':
    flask.run()


def render_create_article():
    return render_template('create.html')


def render_update_article(db, _id):
    item = db.article.find_one({'_id': ObjectId(str(_id))})
    item = json.loads(MongoJSONEncoder().encode(item))

    return render_template('update.html', article=item)


def login():
    return render_template('login.html')


# retrieve all articles
flask.add_url_rule('/articles', 'article_management_list', partial(list_articles, flask.db), methods=['GET'])

# get detail article
flask.add_url_rule(
    '/articles/<_id>/detail', 'article_detail_detail', partial(detail_article, flask.db), methods=['GET']
)

# render create article
flask.add_url_rule('/create', 'render_create_article', render_create_article, methods=['GET'])
# Call create article
flask.add_url_rule(
    '/articles/create', 'article_management_create', partial(create_article, flask.db), methods=['POST']
)


# redner update article
flask.add_url_rule(
    '/articles/<_id>/update', 'article_detail_update', partial(render_update_article, flask.db), methods=['GET']
)
# call update article
flask.add_url_rule(
    '/articles/<_id>/update/call', 'article_detail_update_call', partial(update_article, flask.db), methods=['POST']
)

# call delete article
flask.add_url_rule(
    '/articles/<_id>/delete', 'article_detail_delete', partial(delete_article, flask.db), methods=['GET']
)

# call create article comment
flask.add_url_rule(
    '/articles/<_id>/comments', 'article_detail_create_comment',
    partial(update_comment_article, flask.db), methods=['post']
)
