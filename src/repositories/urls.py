from src.models.urls import Url
from src.clients.redis_client import RedisClient


class UrlRepository:

    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    def create_url(self):
        pass

    def get_url_by_key(self, key: str):
        pass
