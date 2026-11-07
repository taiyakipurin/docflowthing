from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Text, Integer, UniqueConstraint
from datetime import datetime

from app.core.database import Base

class JobServerResult(Base):
    __tablename__ = 'job_server_results'

    __table_args__ = (
        UniqueConstraint(
            'job_id',
            'server_id',
            name='uq_job_server_result'
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    job_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('automation_jobs.id'),
        nullable=False
    )

    server_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('servers.id'),
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    stdout: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    stderr: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    job: Mapped['AutomationJob'] = relationship(
        back_populates='server_results'
    )

    server: Mapped['Server'] = relationship(
        back_populates='job_results'
    )

