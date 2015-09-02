import redis

class Redis():

    def __init__(self, host, port):
        self._client = redis.StrictRedis(host=host, port=port, db=0)

    def get(self, tag):
        return self._client.lrange(tag, 0, -1)

