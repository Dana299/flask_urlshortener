from typing import Optional

import redis

from src.clients.abstract_client import AbstractClient
from src.exceptions import RedisConnectionError


class RedisClient(AbstractClient):

    def __init__(self, redis_dsn: str):
        self.redis_dsn = redis_dsn
        self.conn = None

    def connect(self):
        if not self.conn:
            try:
                self.conn = redis.Redis.from_url(self.redis_dsn, decode_responses=True)
                self.conn.ping()
            except redis.ConnectionError:
                raise

    def set(self, key: str, mapping: dict, ttl: Optional[int] = None):
        """Set a dict in the hash with a TTL (time to live)."""
        if not self.conn:
            raise RedisConnectionError("No connection with redis established")
        self.conn.hset(key, mapping=mapping)
        if ttl:
            self.conn.expire(key, ttl)

    def get(self, key: str):
        """Get the value in a hash stored at key."""
        if not self.conn:
            raise RedisConnectionError("No connection with redis established")
        return self.conn.hgetall(key)


if __name__ == '__main__':
    client = RedisClient("redis://localhost:6379")
    client.connect()