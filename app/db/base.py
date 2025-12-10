from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """abstract base class for all ORM models"""

    __abstract__ = True

    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="when post created",
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="when post updated",
    )
