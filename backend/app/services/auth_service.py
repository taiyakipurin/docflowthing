from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.redis_service import store_refresh
from app.core.config import settings
from app.core.security import create_refresh_token
from app.core.exceptions import InvalidCredentialsError

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

    store_refresh(refresh_token, user.id, settings.refresh_token_ttl)

    return TokenResponse(access_token=access_token), refresh_token

def get_me(current_user: User) -> UserResponse:
    return UserResponse.model_validate(current_user)