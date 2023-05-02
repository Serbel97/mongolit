import math
import json
from typing import List

from flask import jsonify

from apps.encoders import MongoJSONEncoder


def single_response(item: dict, http_status: int):
    return jsonify({'response': item}), http_status


def pagination_response(items: List[dict], http_status: int, page: int = 1, limit: int = 10, total: int = 1):
    items = json.loads(MongoJSONEncoder().encode(items))
    metadata = {
        'page': page,
        'limit': limit,
        'pages': math.ceil(total / limit),
        'total': total
    }

    return jsonify({'items': items, 'metadata': metadata}), http_status
