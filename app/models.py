from datetime import datetime

from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
)

from database import Base


class Url(Base):
    __tablename__ = "urls"

    short_code: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
