from datetime import datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Url:
    __tablename__ = "urls"

    short_code: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
