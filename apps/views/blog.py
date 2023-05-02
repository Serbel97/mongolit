from bson import ObjectId

from flask import render_template, request

from apps.resposne import pagination_response, single_response
from apps.views.base import BaseView


class BlogManagement(BaseView):
    def post(self):
        data = request.get_json()
        result = self._db.articles.insert_one(data)
        if result.acknowledged:
            items = []
            for article in self._db.articles.find().limit(10):
                items.append(article)
            return pagination_response(items, 201)
        else:
            return single_response({"status": "error", "message": "Document not crated"}, 400)

    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        total = self._db.articles.count_documents({})

        items = []
        articles = self._db.articles.find().sort('_id', -1).skip(limit * (page - 1)).limit(limit)
        for article in articles:
            items.append(article)

        return pagination_response(items, 200, page, limit, total)


class BlogDetail(BaseView):
    def _get_item(self, _id):
        return self._db.articles.find_one({'_id': ObjectId(str(_id))})

    def get(self, _id: int):
        article = self._get_item(_id)
        return render_template("index.html", article=article)

    def put(self, _id: int):
        data = request.get_json()
        result = self._db.articles.update_one({"_id": _id}, {"$set": data})

        if result.matched_count > 0:
            article = self._get_item(_id)
            return single_response(article, 200)
        else:
            return single_response({"status": "error", "message": "Document not found"}, 404)

    def delete(self, _id: int):
        result = self._db.articles.delete_one({"_id": _id})
        if result.matched_count > 0:
            items = []
            for article in self._db.articles.find().limit(10):
                items.append(article)
            return pagination_response(items, 200)
        else:
            return single_response({"status": "error", "message": "Document not found"}, 404)
