from pydantic import BaseModel
from pydantic import HttpUrl


class Url(BaseModel):
    url_key: str
    full_url: HttpUrl
    short_url: HttpUrl