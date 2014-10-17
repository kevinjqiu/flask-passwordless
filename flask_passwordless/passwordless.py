import uuid
import hashlib
from .delivery_method import DeliverByMandrill


class UserProvider(object):
    def get_user_by_id(self, userid):
        return hashlib.sha1(userid).hexdigest()


class TokenStore(object):
    STORE = {}

    def store_or_update(self, token, userid, ttl=600, origin=None):
        self.STORE[userid] = token

    def invalidate_token(self, userid):
        del self.STORE[userid]

    def get_by_userid(self, userid):
        return self.STORE.get(userid, None)


class Passwordless(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.user_provider = UserProvider()
        self.token_store = TokenStore()
        self.delivery_method = DeliverByMandrill(app.config)

    def request_token(self, user):
        userid = self.user_provider.get_user_by_id(user)
        token = uuid.uuid4().hex
        self.token_store.store_or_update(token, userid)
        self.delivery_method(token, userid, email=user)

    def authenticate(self, token, userid):
        is_authenticated = self.token_store.get_by_userid(userid) == token
        if is_authenticated:
            self.token_store.invalidate_token(userid)

        return is_authenticated
