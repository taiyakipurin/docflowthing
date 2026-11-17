from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.redis_service import store_refresh_token, consume_refresh_token, delete_refresh_token
from app.core.config import settings
from app.core.security import create_refresh_token
from app.core.exceptions import InvalidCredentialsError, InvalidRefreshTokenError

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.scalar(
        select(User).where(
            User.username == username
        )
    )

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user

def login_user(db: Session, username: str, password: str) -> tuple[TokenResponse, str]:
    user = authenticate_user(db, username, password)

    if user is None:
        raise InvalidCredentialsError

    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token()

    store_refresh_token(refresh_token, user.id, settings.refresh_token_ttl)

    return TokenResponse(access_token=access_token), refresh_token

def get_me(current_user: User) -> UserResponse:
    return UserResponse.model_validate(current_user)

def refresh_user(refresh_token: str, db: Session) -> tuple[TokenResponse, str] | None:
    user_id = consume_refresh_token(refresh_token)

    if user_id is None:
        return None

    user = db.scalar(select(User).where(User.id == user_id)).first()

    if user is None or not user.is_active:
        return None

    access_token = create_access_token(user.id, user.username)
    new_refresh_token = create_refresh_token()

    store_refresh_token(refresh_token, user.id, settings.refresh_token_ttl)

    return TokenResponse(access_token=access_token), new_refresh_token

def logout_user(refresh_token: str) -> None:
    if refresh_token is None:
        return

    delete_refresh_token(refresh_token)
