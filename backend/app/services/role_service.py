from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import RoleNotFoundError
from app.models.role import Role
from app.schemas.role import RoleResponse

def get_roles(db: Session) -> list[RoleResponse]:
    roles = db.scalars(
        select(Role).order_by(Role.id)
    ).all()

    return [RoleResponse.model_validate(role) for role in roles]

def get_role(db: Session, role_id: int) -> RoleResponse:
    role = db.scalar(
        select(Role).where(
            Role.id == role_id
        )
    )

    if role is None:
        raise RoleNotFoundError

    return RoleResponse.model_validate(role)