from flask.views import MethodView


class BaseView(MethodView):
    init_every_request = False

    def __init__(self, db):
        self._db = db
