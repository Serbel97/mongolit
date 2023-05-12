from functools import wraps

from bson import ObjectId
from flask import request, redirect, url_for, session

from apps.user_role import UserRole


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


def require_admin(f):
    @wraps(f)
    def decorated(db, *args, **kwargs):
        user = request.user

        if user['group'] == UserRole.ADMIN.value[0]:
            return f(db, *args, **kwargs)
        return redirect(url_for('article_management_list'))
    return decorated
