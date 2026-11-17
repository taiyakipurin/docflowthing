from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Response, Cookie, status

from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.core.database import get_db
from app.services.auth_service import login_user, get_me, refresh_user, logout_user
from app.api.dependencies import get_current_user
from app.models import User
from app.core.config import settings
from app.core.exceptions import InvalidRefreshTokenError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/login', response_model=TokenResponse)
def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    token_response, refresh_token = login_user(db, **login_data.model_dump())

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False, #!note: set true later
        samesite='lax',
        max_age=settings.refresh_token_ttl,
        path='/api/v1/auth'
    )

    return token_response

@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None)
):
    logout_user(refresh_token)

    response.delete_cookie(
        key='refresh_token',
        httponly=True,
        secure=False, #!note: set true later
        samesite='lax',
        path='/api/v1/auth'
    )

    response.status_code=status.HTTP_204_NO_CONTENT


@router.post('/refresh', response_model=TokenResponse)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if refresh_token is None:
        return InvalidRefreshTokenError

    token_response, new_refresh_token = refresh_user(refresh_token, db)

    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        secure=False, #!note: set true
        samesite='lax',
        max_age=settings.refresh_token_ttl,
        path='/api/v1/auth'
    )

    return token_response



@router.get('/me', response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return get_me(user)