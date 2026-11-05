from sqlalchemy import BigInteger, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.associations.document_server import document_servers

from datetime import datetime

class Server(Base):
    __tablename__ = 'servers'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default='active',
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    documents: Mapped[list['InfrastructureDocument']] = relationship(
        secondary=document_servers,
        back_populates='servers'
    )