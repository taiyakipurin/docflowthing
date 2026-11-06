from sqlalchemy import String, BigInteger, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base

from app.models.associations.user_role import user_roles
# from app.models.approval_decision import ApprovalDecision


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
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

    roles: Mapped[list['Role']] = relationship(
        'Role',
        secondary=user_roles,
        back_populates='users'
    )

    approval_decisions: Mapped[list['ApprovalDecision']] = relationship(
        back_populates='approver',
    )