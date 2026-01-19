from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Message(BaseModel):
    message: str


class UrlOut(BaseModel):
    long_url: HttpUrl
    short_code: str
    created_at: datetime
