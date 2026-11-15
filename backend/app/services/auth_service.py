from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponse
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

def login_user(db: Session, username: str, password: str) -> TokenResponse:
    user = authenticate_user(db, username, password)

    if user is None:
        raise InvalidCredentialsError

    access_token = create_access_token(user.id, user.username)

    return TokenResponse(access_token=access_token)
