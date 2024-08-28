import hashlib
from typing import Optional

from pydantic import HttpUrl

from src.clients.redis_client import RedisClient
from src.models.urls import Url


class UrlRepository:

    def __init__(self, redis_client: RedisClient, service_base_url: str):
        self.redis_client = redis_client
        self.service_base_url = service_base_url

    def create_url(self, url: HttpUrl, min_key_len=6) -> Url:
        collision = True
        while collision:
            key = self._generate_hash(str(url), min_key_len)
            collision = bool(self.redis_client.get_dict_by_key(key))
            min_key_len += 1
        short_url = f"{self.service_base_url}/{key}"
        url_object = Url(url_key=key, full_url=url, short_url=short_url)
        url = self.redis_client.set_dict_with_ttl(
            key,
            {k: str(v) for k, v in url_object.model_dump().items()},
            ttl=None
        )
        return url_object

    def get_url_by_key(self, key: str) -> Optional[str]:
        url_data = self.redis_client.get_dict_by_key(key)
        if url_data:
            url_object = Url(**url_data)
            return url_object.full_url
        return None

    @staticmethod
    def _generate_hash(data: str, key_len: int) -> str:
        """Generates a key with a given length from data."""
        encoded_url = data.encode('utf-8')
        sha256_url_hash = hashlib.sha256(encoded_url)
        return sha256_url_hash.hexdigest()[:key_len]
