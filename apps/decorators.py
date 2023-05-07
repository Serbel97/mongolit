from functools import wraps

from bson import ObjectId
from flask import request, redirect, url_for, session


def require_auth(f):
    @wraps(f)
    def decorated(db, *args, **kwargs):
        auth_header = session.get('Authorization', None)

        if auth_header:
            user = db.user.find_one({'_id': ObjectId(auth_header)})

            if user:
                setattr(request, 'user', user)
                return f(db, *args, **kwargs)

        return redirect(url_for('login'))

    return decorated
