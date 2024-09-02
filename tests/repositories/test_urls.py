import hashlib

from pydantic import HttpUrl

from src.clients.abstract_client import AbstractClient
from src.repositories.urls import UrlRepository


class FakeRedisClient(AbstractClient):

    def __init__(self, items: dict = {}):
        self._items = items

    def connect(self):
        pass

    def set(self, key, value, ttl=None):
        self._items[key] = value

    def get(self, key: str):
        return self._items.get(key, {})

    def get_all(self):
        return self._items.values()


SERVICE_BASE_URL = "http://clicker.ru"
MIN_KEY_LEN = 6


def test_create_valid_url():
    fake_redis = FakeRedisClient()
    test_repo = UrlRepository(fake_redis, SERVICE_BASE_URL)

    url_object = test_repo.create_url(url=HttpUrl("http://longurl.com"))

    assert url_object is not None
    assert str(url_object.full_url).rstrip("/") == "http://longurl.com"
    assert str(url_object.short_url).startswith(SERVICE_BASE_URL)

    url = test_repo.redis_client.get(str(url_object.url_key))
    assert url["full_url"].rstrip("/") == "http://longurl.com"
    assert url["url_key"] == str(url_object.short_url).split("/")[-1]
    assert url["short_url"] == str(url_object.short_url)


def test_create_existing_url():
    fake_redis = FakeRedisClient()
    test_repo = UrlRepository(fake_redis, SERVICE_BASE_URL)

    existing_url = HttpUrl("http://longurl.com")

    # duplicates creation
    url_object_1 = test_repo.create_url(url=existing_url)
    url_object_2 = test_repo.create_url(url=existing_url)

    assert url_object_2 is not None
    assert url_object_2.full_url == url_object_1.full_url
    assert url_object_2.short_url == url_object_1.short_url

    assert len(list(fake_redis.get_all())) == 1


def test_create_url_with_collision():
    url_1 = "http://example.com/"
    url_2 = "http://anotherexample.com/"
    collision_key = hashlib.sha256(url_2.encode("utf-8")).hexdigest()[:MIN_KEY_LEN]
    fake_client = FakeRedisClient({
        collision_key: {
            "full_url": url_1,
            "short_url": f"{SERVICE_BASE_URL}/{collision_key}",
            "url_key": collision_key
        }
    })

    collision_test_repo = UrlRepository(fake_client, SERVICE_BASE_URL)
    collision_url_object = collision_test_repo.create_url(HttpUrl(url_2))

    assert len(collision_url_object.url_key) == MIN_KEY_LEN + 1
    assert len(fake_client.get_all()) == 2
