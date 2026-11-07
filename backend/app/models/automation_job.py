from sqlalchemy import BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.core.database import Base
from app.models.infrastructure_document import InfrastructureDocument


class AutomationJob(Base):
    __tablename__ = 'automation_jobs'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    scenario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('automation_scenarios.id'),
        nullable=False
    )

    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('infrastructure_documents.id'),
        nullable=False
    )

    launched_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default='pending',
        nullable=False
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    scenario: Mapped['AutomationScenario'] = relationship(
        back_populates='automation_jobs'
    )

    document: Mapped['InfrastructureDocument'] = relationship(
        back_populates='automation_jobs'
    )

    launcher: Mapped['User'] = relationship(
        back_populates='automation_jobs'
    )

    server_results: Mapped[list['JobServerResult']] = relationship(
        back_populates='job'
    )

    execution_acts: Mapped[list['ExecutionAct']] = relationship(
        back_populates='job'
    )