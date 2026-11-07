from sqlalchemy import BigInteger, String, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Any

from app.core.database import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    details: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    auditor: Mapped['User | None'] = relationship(
        back_populates='audit_logs'
    )