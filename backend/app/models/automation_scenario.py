from sqlalchemy import BigInteger, String, DateTime, Boolean, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base
from app.models.automation_job import AutomationJob


class AutomationScenario(Base):
    __tablename__ = 'automation_scenarios'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    playbook_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    automation_jobs: Mapped[list[AutomationJob]] = relationship(
        back_populates='scenario'
    )