import abc


class TokenStore(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        pass

    @abc.abstractmethod
    def store_or_update(self, token, userid, ttl=600, origin=None):
        return

    @abc.abstractmethod
    def invalidate_token(self, userid):
        return

    @abc.abstractmethod
    def get_by_userid(self, userid):
        return


class MemoryTokenStore(TokenStore):
    STORE = {}

    def store_or_update(self, token, userid, ttl=600, origin=None):
        self.STORE[userid] = token

    def invalidate_token(self, userid):
        del self.STORE[userid]

    def get_by_userid(self, userid):
        return self.STORE.get(userid, None)


class RedisTokenStore(TokenStore):

    def __init__(self, host, tokenspace):
        import redis
        if not host:
            self.host = "localhost"
        if not tokenspace:
            self.tokenspace = 'logintokens'
        self.Redis = redis.StrictRedis(host=host)

    def store_or_update(self, token, userid, ttl=600, origin=None):
        # set TTL on key?
        self.Redis.hset(self.tokenspace, userid, token)

    def invalidate_token(self, userid):
        self.Redis.hdel(self.tokenspace, userid)

    def get_by_userid(self, userid):
        return self.Redis.hget(self.tokenspace, userid, None)


class MongoTokenStore(TokenStore):
    STORE = {}

    def __init__(self, config):
        from pymongo import MongoClient
        self.db = MongoClient(config['url'])
        self.origin = config['origin']
        self.ttl = config['ttl']

    def store_or_update(self, token, userid, ttl=None, origin=None):
        if not token:
            return False
        if not userid:
            return False
        if origin:
            if origin != self.origin:
                return False
        if not ttl:
            ttl = self.ttl

        self.STORE[userid] = token

    def invalidate_token(self, userid):
        del self.STORE[userid]

    def get_by_userid(self, userid):
        return self.STORE.get(userid, None)


TOKEN_STORES = {
    'memory': MemoryTokenStore,
    'redis': RedisTokenStore,
    'mongo': MongoTokenStore
}
