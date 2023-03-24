from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Uuid, Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    id = Column(Uuid, primary_key=True, default=uuid4)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
