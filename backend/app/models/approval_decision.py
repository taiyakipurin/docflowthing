from sqlalchemy import ForeignKey, BigInteger, String, Text, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.core.database import Base
# from app.models.infrastructure_document import InfrastructureDocument


class ApprovalDecision(Base):
    __tablename__ = 'approval_decisions'

    id: Mapped[int] = mapped_column(
        BigInteger,
        autoincrement=True,
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('infrastructure_documents.id'),
        nullable=False
    )

    approver_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False
    )

    decision: Mapped[str] = mapped_column(
        String(50),
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    document: Mapped['InfrastructureDocument'] = relationship(
        back_populates='approval_decisions',
    )

    approver: Mapped['User'] = relationship(
        back_populates='approval_decisions',
    )