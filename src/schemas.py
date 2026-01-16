from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Message(BaseModel):
    message: str


class UrlIn(BaseModel):
    long_url: HttpUrl


class Url(UrlIn):
    short_code: str
    created_at: datetime


class ShortCodeOut(BaseModel):
    short_code: str
