from uuid import uuid4

from sqlalchemy import Boolean, Column, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import BaseModel


class User(BaseModel):
    """
    User model
    Basic info about a client of bank
    """

    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="ID user",
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Email user",
    )
    first_name = Column(
        String(100),
        nullable=False,
        comment="First name",
    )
    last_name = Column(
        String(100),
        nullable=False,
        comment="Last name",
    )
    password_hash = Column(
        String(255),
        nullable=False,
        comment="Hash password",
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Check for active user or not",
    )
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Check what user is verified",
    )

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_is_active", "is_active"),
    )

    def __repr__(self) -> str:
        f"User(user_id={self.user_id}, email={self.email})"
