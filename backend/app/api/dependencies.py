from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import jwt

from app.core.security import decode_access_token
from app.core.database import get_db
from app.models import User

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    try:
        decoded_token = decode_access_token(credentials.credentials)
        user_id = int(decoded_token['sub'])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    user = db.scalar(
        select(User).where(
            User.id == user_id
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    return user

def require_roles(*required_roles):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_roles = {role.code for role in current_user.roles}

        if not (set(required_roles) & user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Action not allowed'
            )

        return current_user

    return role_checker