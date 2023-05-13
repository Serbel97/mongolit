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
    add_comment_article
from apps.views.auth import auth, logout, signup
from apps.views.user import users_me, update_user, update_user_password, list_users, delete_user, update_user_group

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class FlaskProject(Flask):
    def __init__(self, __name__):

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
flask.secret_key = 'your_secret_key'

if __name__ == '__main__':
    flask.run()


def render_create_article():
    return render_template('article/create.html')


def render_update_article(db, _id):
    item = db.article.find_one({'_id': ObjectId(str(_id))})
    item = json.loads(MongoJSONEncoder().encode(item))

    return render_template('article/update.html', article=item)


def login():
    return render_template('auth_forms/login.html')


def render_register():
    return render_template('auth_forms/register.html')


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
    partial(add_comment_article, flask.db), methods=['post']
)

flask.add_url_rule('/', 'login', login, methods=['GET'])
flask.add_url_rule('/auth', 'auth', partial(auth, flask.db), methods=['POST'])
flask.add_url_rule('/logout', 'logout', partial(logout, flask.db), methods=['GET'])
flask.add_url_rule('/signup', 'signup', partial(signup, flask.db), methods=['POST'])

flask.add_url_rule('/users/me', 'user_profile', partial(users_me, flask.db), methods=['GET'])
flask.add_url_rule('/users/<_id>/update', 'user_update', partial(update_user, flask.db), methods=['POST'])
flask.add_url_rule(
    '/users/<_id>/update/password', 'user_update_pwd', partial(update_user_password, flask.db), methods=['POST']
)

flask.add_url_rule('/register', 'auth_form', render_register, methods=['GET'])

flask.add_url_rule('/admin/users', 'admin_users', partial(list_users, flask.db), methods=['GET'])
flask.add_url_rule(
    '/admin/users/<_id>/delete', 'admin_users_delete', partial(delete_user, flask.db), methods=['GET']
)
flask.add_url_rule(
    '/admin/users/<_id>/group/<group>', 'admin_users_group', partial(update_user_group, flask.db), methods=['GET']
)
