import json

from flask import request, redirect, url_for, session

from apps.encoders import MongoJSONEncoder


def auth(db):
    data = {
        'email': request.form['email'],
        # 'password': request.form['password'],
    }

    user = db.user.find_one(data)
    user = json.loads(MongoJSONEncoder().encode(user))

    session['Authorization'] = user['_id']

    return redirect(url_for('article_management_list'))


def logout():
    if 'Authorization' in session:
        del session['Authorization']
    return redirect(url_for('login'))


def signup():
    pass
