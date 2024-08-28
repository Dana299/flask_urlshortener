import json

from flask import Blueprint, Response, jsonify, redirect, request
from pydantic import HttpUrl, ValidationError

from src.repositories.urls import UrlRepository


def create_url_routes(repo: UrlRepository):
    bp = Blueprint("url_routes", __name__)

    @bp.route('/<url_key>', methods=['GET'])
    def get_url(url_key):
        full_url = repo.get_url_by_key(url_key)
        if not full_url:
            return Response(status=404)
        return redirect(full_url, code=200)

    @bp.route('/', methods=['POST'])
    def create_url():
        url = request.form.get('url')
        if not url:
            return Response(status=400)
        try:
            url = HttpUrl(url)
            short_url = repo.create_url(url)
            return jsonify(success=json.loads(short_url.model_dump_json())), 201
        except ValidationError:
            return Response(status=400, response="Not a valid url")

    return bp
