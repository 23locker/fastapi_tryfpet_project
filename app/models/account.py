from enum import Enum as PythonEnum
from uuid import uuid4

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import BaseModel


class AccountType(str, PythonEnum):
    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"


class AccountStatus(str, PythonEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    CLOSED = "closed"


class Account(BaseModel):
    __tablename__ = "accounts"

    account_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="Unique ID bank account",
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
        index=True,
        comment="ID owner bank account",
    )

    account_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        comment="Number of bank account",
    )

    account_type = Column(
        Enum(AccountType),
        nullable=False,
        default=AccountType.CHECKING,
        comment="Type of bank account (checking, saving, investment)",
    )

    balance = Column(
        Float,
        nullable=False,
        default=0.0,
        comment="Balance of bank accountt",
    )

    currency = Column(
        String(3),
        nullable=False,
        default="USD",
        comment="Account currency",
    )

    status = Column(
        Enum(AccountStatus),
        nullable=False,
        default=AccountStatus.ACTIVE,
        comment="Status a bank account",
    )

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Check what bank account is primary or not",
    )

    __table_args__ = (
        Index("idx_account_user_id", "user_id"),
        Index("idx_account_status", "status"),
        Index("idx_account_currency", "currency"),
    )

    def __repr__(self) -> str:
        return f"<Account(account_id={self.account_id}, number={self.account_number}, balance={self.balance})>"
