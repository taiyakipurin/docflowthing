from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from app.schemas.auth import LoginRequest, TokenResponse
from app.core.database import get_db
from app.services.auth_service import login_user

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

@router.get('/me')
def me():
    pass