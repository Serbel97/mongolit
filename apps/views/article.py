import json
import math
from datetime import datetime

from bson import ObjectId

from flask import render_template, request, redirect, url_for

from apps.decorators import require_auth
from apps.encoders import MongoJSONEncoder


@require_auth
def list_articles(db):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 9))
    total = db.article.count_documents({})

    items = []
    articles = db.article.find().sort('date', -1).skip(limit * (page - 1)).limit(limit)
    for article in articles:
        article['text'] = article['text'][:25] + '...'
        items.append(article)

    items = json.loads(MongoJSONEncoder().encode(items))

    pages = math.ceil(total / limit)

    return render_template(
        'index.html',
        articles=items,
        prev_page=1 if page - 1 == 0 else page - 1,
        next_page=pages if page + 1 > pages else page + 1,
    )


@require_auth
def create_article(db):
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'text': request.form['text_area_content'],
        'category': request.form.getlist('category'),
        'author_id': request.user['_id']
    }

    db.article.insert_one(data)
    return redirect(url_for('article_management_list'))


@require_auth
def update_article(db, _id):
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'text': request.form['text_area_content'],
        'category': request.form.getlist('category'),
    }

    db.article.update_one({'_id': ObjectId(str(_id))}, {'$set': data})

    return redirect(url_for('article_detail_detail', _id=_id))


@require_auth
def update_comment_article(db, _id):
    data = {
        'comment': request.form['text_comment'],
        'author': request.user['_id'],
        'date': datetime.now()
    }

    db.article.update_one({'_id': ObjectId(str(_id))}, {'$push': {'comments': data}})

    return redirect(url_for('article_detail_detail', _id=_id))


@require_auth
def delete_article(db, _id):
    db.article.delete_one({'_id': ObjectId(str(_id))})
    return redirect(url_for('article_management_list'))


@require_auth
def detail_article(db, _id):
    pipeline = [
        {
            "$match": {
                "_id": ObjectId(_id)
            }
        },
        {
            "$lookup": {
                "from": "user",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$unwind": {
                "path": "$author",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$comments",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "user",
                "localField": "comments.author",
                "foreignField": "_id",
                "as": "comments.commenter"
            }
        },
        {
            "$unwind": {
                "path": "$comments.commenter",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "date": {"$first": "$date"},
                "text": {"$first": "$text"},
                "author_id": {"$first": "$author_id"},
                "category": {"$first": "$category"},
                "author": {"$first": "$author"},
                "comments": {
                    "$push": {
                        "$cond": [
                            {"$eq": ["$comments", {}]},
                            None,
                            "$comments"
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "name": 1,
                "date": 1,
                "text": 1,
                "author_id": 1,
                "category": 1,
                "author.name": 1,
                "author.email": 1,
                "comments.comment": 1,
                "comments.date": 1,
                "comments.commenter.name": 1,
                "comments.commenter.email": 1
            }
        }
    ]

    result = db.article.aggregate(pipeline)

    item = next(result, None)

    return render_template('detail.html', article=item)
