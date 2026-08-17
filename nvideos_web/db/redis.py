# REDIS
from redis import ConnectionPool, Redis

# FLASK
from flask import Flask

class RedisPool:
    _pool: ConnectionPool | None = None
    _client: Redis | None = None

    def init_app(self, app: Flask):
        self._pool = ConnectionPool.from_url(app.config["REDIS_ADDRESS"])
        self._client = Redis(connection_pool=self._pool)        

    @property
    def client(self):
        if self._client is None:
            raise Exception("Redis cannot be None.")
        return self._client

nredis = RedisPool()