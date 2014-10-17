import uuid
import hashlib
from flask import url_for
from .delivery_method import DELIVERY_METHODS


class TokenStore(object):
    STORE = {}

    def store_or_update(self, token, userid, ttl=600, origin=None):
        self.STORE[userid] = token

    def invalidate_token(self, userid):
        del self.STORE[userid]

    def get_by_userid(self, userid):
        return self.STORE.get(userid, None)


class LoginURL(object):
    def generate(self, token, userid):
        return "".join([
            url_for('authenticate', _external=True),
            "?token={}&uid={}".format(token, userid)
        ])

    def parse(self, request):
        token = request.values['token']
        uid = request.values['uid']
        return token, uid


class Passwordless(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.token_store = TokenStore()

        delivery_method = app.config['PASSWORDLESS']['DELIVERY_METHOD']
        self.delivery_method = DELIVERY_METHODS[delivery_method](app.config)

        # login_url = app.config['PASSWORDLESS']['LOGIN_URL']
        self.login_url = LoginURL()

    def request_token(self, user):
        token = uuid.uuid4().hex
        self.token_store.store_or_update(token, user)
        self.delivery_method(
            self.login_url.generate(token, user),
            email=user
        )

    def authenticate(self, flask_request):
        token, uid = self.login_url.parse(flask_request)
        is_authenticated = self.token_store.get_by_userid(uid) == token
        if is_authenticated:
            self.token_store.invalidate_token(userid)

        return is_authenticated
