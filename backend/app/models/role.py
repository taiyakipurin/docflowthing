from sqlalchemy import BigInteger, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

from app.models.associations import user_roles

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False, 
        unique=True
    )
    
    users: Mapped[list['User']] = relationship(
        'User',
        secondary=user_roles,
        back_populates='roles'
    )