from datetime import datetime
from xml.dom.minidom import Document

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, ForeignKey, func, String

from app.core.database import Base
from app.models.infrastructure_document import InfrastructureDocument


class ExecutionAct(Base):
    __tablename__ = 'execution_acts'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('infrastructure_documents.id'),
        nullable=False
    )

    job_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('automation_jobs.id'),
        nullable=True
    )

    generated_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    document: Mapped['InfrastructureDocument'] = relationship(
        back_populates='execution_acts'
    )
    creator: Mapped['User'] = relationship(
        back_populates='execution_acts'
    )

    job: Mapped['AutomationJob'] = relationship(
        back_populates='execution_acts'
    )