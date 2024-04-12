import json
import math

import bcrypt
from bson import ObjectId
from flask import render_template, request, redirect, url_for

from apps.checkers.user import UserObjectChecker
from apps.decorators import require_auth, require_admin
from apps.encoders import MongoJSONEncoder
from apps.user_role import UserRole


@require_auth
def users_me(db):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 9))
    total = db.article.count_documents({'author_id': request.user['_id']})

    query = request.args.get('query', {})
    if query:
        query = {'name': {'$regex': query, '$options': 'i'}}
    query['author_id'] = request.user['_id']

    articles = db.article.find(query).sort('date', -1).skip(limit * (page - 1)).limit(limit)

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
        total=total,
        user_role=UserRole
    )


@require_auth
def update_user(db, _id):
    user = db.user.find_one({'_id': ObjectId(str(_id))})
    if not UserObjectChecker.user(request_user=request.user, user=user):
        return redirect(url_for('article_management_list'))
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
    }

    db.user.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('user_profile'))


@require_auth
def update_user_password(db, _id):
    user = db.user.find_one({'_id': ObjectId(str(_id))})
    if not UserObjectChecker.user(request_user=request.user, user=user):
        return redirect(url_for('article_management_list'))

    password = request.form['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    data = {
        'password': hashed_password.decode('utf-8')
    }

    db.user.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('user_profile'))


@require_auth
@require_admin
def list_users(db):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    total = db.user.count_documents({})

    query = request.args.get('query', {})
    if query:
        query = {'name': {'$regex': query, '$options': 'i'}}

    items = []
    users = db.user.find(query).sort('name', -1).skip(limit * (page - 1)).limit(limit)
    for user in users:
        items.append(user)

    items = json.loads(MongoJSONEncoder().encode(items))

    pages = math.ceil(total / limit)

    return render_template(
        'admin/users.html',
        users=items,
        prev_page=1 if page - 1 == 0 else page - 1,
        next_page=pages if page + 1 > pages else page + 1,
        user_role=UserRole
    )


@require_auth
@require_admin
def delete_user(db, _id):
    db.article.delete_many({'author_id': ObjectId(str(_id))})
    db.user.delete_one({'_id': ObjectId(str(_id))})
    return redirect(url_for('admin_users'))


@require_auth
@require_admin
def update_user_group(db, _id, group):
    data = {
        'group': int(group),
    }

    db.user.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('admin_users'))
