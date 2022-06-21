import redis


class RedisConnector:
    def __init__(self, access_key: str, host: str = 'locahost', port: int = 6379, db: int = 0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=access_key, ssl=True)

    def ping(self):
        result = self.redis.ping()
        print("Ping returned : " + str(result))

    def hset(self, name: str, key: str, value: str | float | int):
        return self.redis.hset(name=name, key=key, value=value)

    def hget(self, name: str, key: str):
        return self.redis.hget(name=name, key=key)

    def hdel(self, name: str):
        all_keys = list(self.redis.hgetall(name).keys())
        if all_keys:
            return self.redis.hdel(name, *all_keys)
        else:
            return 0
