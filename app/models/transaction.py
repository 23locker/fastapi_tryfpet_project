from enum import Enum as PythonEnum
from uuid import uuid4

from sqlalchemy import Column, Enum, Float, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import BaseModel


class TransactionType(str, PythonEnum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PAYMENT = "payment"


class TransactionStatus(str, PythonEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(BaseModel):
    __tablename__ = "transaction"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="unique ID transaction",
    )

    from_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.account_id"),
        nullable=False,
        index=True,
        comment="ID bank account",
    )

    transaction_type = Column(
        Enum(TransactionType),
        nullable=False,
        comment="Type of transaction",
    )

    amount = Column(
        Float,
        nullable=False,
        comment="Amount of transaction",
    )

    currency = Column(
        String(3),
        nullable=False,
        default="USD",
        comment="Transaction currency",
    )

    status = Column(
        Enum(TransactionStatus),
        nullable=False,
        default=TransactionStatus.PENDING,
        comment="Transaction status",
    )

    description = Column(
        Text,
        nullable=True,
        comment="Transaction description",
    )

    reference_number = Column(
        String(50),
        nullable=True,
        unique=True,
        comment="Tracking reference number",
    )

    __table_args__ = (
        Index("idx_transaction_from_account", "from_account_id"),
        Index("idx_transaction_to_account", "to_account_id"),
        Index("idx_transaction_status", "status"),
        Index("idx_transaction_type", "transaction_type"),
    )

    def __repr__(self) -> str:
        return f"<Transaction(transaction_id={self.transaction_id}, amount={self.amount}, status={self.status})>"
