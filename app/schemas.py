from datetime import datetime

from pydantic import UUID4, BaseModel, HttpUrl


class Message(BaseModel):
    message: str


class UrlOut(BaseModel):
    uuid: UUID4
    long_url: HttpUrl
    short_code: str
    created_at: datetime
