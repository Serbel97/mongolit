import json

import bcrypt

from flask import request, redirect, url_for, session

from apps.decorators import require_auth
from apps.encoders import MongoJSONEncoder


def auth(db):
    user = db.user.find_one({'email': request.form['email']})

    if user:
        # Get the password from the form submission
        request_password = request.form['password'].encode('utf-8')
        stored_password = user['password'].encode('utf-8')  # Encode the stored password
        is_valid_password = bcrypt.checkpw(request_password, stored_password)

        if is_valid_password:
            user = json.loads(MongoJSONEncoder().encode(user))
            session['Authorization'] = user['_id']
            return redirect(url_for('article_management_list'))
    return redirect(url_for('login'))


@require_auth
def logout(db):
    if 'Authorization' in session:
        del session['Authorization']
    return redirect(url_for('login'))


def signup(db):
    password = request.form['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": hashed_password.decode('utf-8')
    }

    db.user.insert_one(user)

    return redirect(url_for('login'))
