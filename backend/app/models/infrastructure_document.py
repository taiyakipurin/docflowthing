from sqlalchemy import BigInteger, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.core.database import Base
# from app.models.approval_decision import ApprovalDecision
from app.models.associations.document_server import document_servers

class InfrastructureDocument(Base):
    __tablename__ = "infrastructure_documents"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    author_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    justification: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default='draft',
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    servers: Mapped[list['Server']] = relationship(
        'Server',
        secondary=document_servers,
        back_populates='documents'
    )

    approval_decisions: Mapped[list['ApprovalDecision']] = relationship(
        back_populates='document'
    )