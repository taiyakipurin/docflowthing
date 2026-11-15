from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.role import RoleResponse
from app.core.database import get_db
from app.services.role_service import (
    get_role as get_role_service,
    get_roles as get_roles_service
)

router = APIRouter(prefix='/roles', tags=['Roles'])

@router.get('/', response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return get_roles_service(db)

@router.get('/{role_id}', response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return get_role_service(db, role_id)
