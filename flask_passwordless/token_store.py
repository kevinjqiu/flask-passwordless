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
        self.Redis.expire(self.tokenspace, ttl)

    def invalidate_token(self, userid):
        self.Redis.hdel(self.tokenspace, userid)

    def get_by_userid(self, userid):
        return self.Redis.hget(self.tokenspace, userid, None)


class MongoTokenStore(TokenStore):
    # TODO: alias collection so we don't call self.db[derp][foo]
    def __init__(self, config):
        from pymongo import MongoClient
        from pymongo.collection import Collection
        if 'dbname' not in config:
            self.dbname = 'tokenstore'
        else:
            self.dbname = config['dbname']
        if 'dbhost' not in config:
            self.dbhost = 'localhost'
        else:
            self.dbhost = config['dbhost']
        if 'dbport' not in config:
            self.dbport = 27017
        else:
            self.dbhost = config['dbhost']
        self.db = MongoClient(self.dbhost, self.dbport)
        if 'collection' not in config:
            self.collection_name = 'tokenstore'
        else:
            self.collection_name = config['collection']
        if 'origin' in config:
            self.origin = config['origin']
        else:
            self.origin = None
        if 'ttl' in config:
            self.ttl = config['ttl']
        else:
            self.ttl = None

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
        self.db[self.dbname][self.collection_name].save({'token': token, 'userid': userid})

    def invalidate_token(self, userid):
        self.db[self.dbname][self.collection_name].remove({'userid': userid})

    def get_by_userid(self, userid):
        usertoken = self.db[self.dbname][self.collection_name].find_one({'userid': userid})
        if 'token' in usertoken:
            return usertoken['token']
        else:
            return None


TOKEN_STORES = {
    'memory': MemoryTokenStore,
    'redis': RedisTokenStore,
    'mongo': MongoTokenStore
}
