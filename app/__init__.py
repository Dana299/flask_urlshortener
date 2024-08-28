import os
from pathlib import Path

import yaml
from flask import Flask

from app.routes import create_url_routes
from src.clients.redis_client import RedisClient
from src.repositories.urls import UrlRepository

BASE_PATH = Path(__file__).resolve().parents[1]


def create_app(config_file: str = "config.yaml"):
    app = Flask(__name__)

    if not os.path.isabs(config_file):
        config_file = os.path.join(BASE_PATH, config_file)

    app.config.from_file(config_file, load=yaml.safe_load)

    SECRET_KEY = os.urandom(12).hex()
    app.config['SECRET_KEY'] = SECRET_KEY

    # creating redis client instance
    redis_client = RedisClient(app.config["REDIS_DSN"])
    redis_client.connect()

    # creating repository instance for urls
    url_repo = UrlRepository(redis_client, app.config["SERVICE_URL"])

    # registration of blueprint
    app.register_blueprint(create_url_routes(url_repo))

    return app
