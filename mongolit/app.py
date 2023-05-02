import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask
from flask_pymongo import pymongo

from apps.views.blog import BlogDetail, BlogManagement


def register_api(app, name):
    blog_management = BlogManagement.as_view(f"{name}-blog_management", flask.db)
    app.add_url_rule(f"/{name}", view_func=blog_management)

    blog_detail = BlogDetail.as_view(f"{name}-blog_detail", flask.db)
    app.add_url_rule(f"/{name}/<_id>", view_func=blog_detail)


class FlaskProject(Flask):
    def __init__(self, __name__):
        BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

        template_dir = os.path.join(BASE_DIR, 'templates')
        super().__init__(__name__, template_folder=template_dir)

        ENV_FILE = os.path.join(BASE_DIR, '.env')
        if os.path.exists(ENV_FILE):
            load_dotenv(dotenv_path=ENV_FILE, verbose=True)
        else:
            exit(0)

        client = pymongo.MongoClient(os.getenv('MONGODB'))
        self.db = client.get_database('blog')


flask = FlaskProject(__name__)

if __name__ == '__main__':
    flask.run()


register_api(flask, 'blogs')
