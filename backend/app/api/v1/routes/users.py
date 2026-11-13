from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserRolesUpdate
)
from app.services.user_service import (
    create_user as create_user_service,
    get_user as get_user_service,
    get_users as get_users_service,
    update_user as update_user_service,
    update_user_role as update_user_role_service,
    delete_user as delete_user_service
)

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', response_model=UserResponse, status_code=201)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db)
):
    return create_user_service(db, data)

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_service(db, user_id)

@router.get('/', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return get_users_service(db)

@router.patch('/{user_id}', response_model=UserResponse)
def update_user(
    data: UserUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    return update_user_service(db, user_id, data)

@router.delete('/{user_id}', response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user_service(db, user_id)

@router.patch('/{user_id}/roles', response_model=UserResponse)
def update_user_role(
        data: UserRolesUpdate,
        user_id: int,
        db: Session = Depends(get_db)
):
    return update_user_role_service(db, user_id, data)