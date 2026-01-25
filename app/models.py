from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
)

table_registry = registry()


@mapped_as_dataclass(table_registry)
class Url:
    __tablename__ = "urls"

    uuid: Mapped[str] = mapped_column(unique=True, primary_key=True)
    long_url: Mapped[str] = mapped_column(unique=True)
    short_code: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
