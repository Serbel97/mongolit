import json
import math

import bcrypt
from bson import ObjectId
from flask import render_template, request, redirect, url_for

from apps.decorators import require_auth
from apps.encoders import MongoJSONEncoder


@require_auth
def users_me(db):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 9))
    total = db.article.count_documents({'author_id': request.user['_id']})

    articles = db.article.find(
        {'author_id': request.user['_id']}
    ).sort('date', -1).skip(limit * (page - 1)).limit(limit)

    items = []
    for article in articles:
        article['text'] = article['text'][:25] + '...'
        items.append(article)

    items = json.loads(MongoJSONEncoder().encode(items))

    pages = math.ceil(total / limit)

    return render_template(
        'user/profile.html',
        user=request.user,
        articles=items,
        prev_page=1 if page - 1 == 0 else page - 1,
        next_page=pages if page + 1 > pages else page + 1,
        total=total
    )


@require_auth
def update_user(db, _id):
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
    }

    db.user.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('user_profile'))


@require_auth
def update_user_password(db, _id):
    password = request.form['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    data = {
        'password': hashed_password.decode('utf-8')
    }

    db.user.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('user_profile'))
