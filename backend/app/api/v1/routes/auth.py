from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.sql.functions import current_user

from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.core.database import get_db
from app.services.auth_service import login_user
from app.services.auth_service import get_me
from app.api.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/login', response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, **login_data.dict())

@router.post('/logout')
def logout():
    pass

@router.post('/refresh')
def refresh():
    pass

@router.get('/me', response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return get_me(user)