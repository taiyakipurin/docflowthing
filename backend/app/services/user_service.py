from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import UserNotFoundError, UserAlreadyExistsError
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserRolesUpdate
from app.core.security import hash_password
from app.models.user import User
from app.models.role import Role

def create_user(db: Session, data: UserCreate) -> UserResponse:
    password_hash = hash_password(data.password)

    user = User(
        **data.model_dump(exclude={'password'}),
        password_hash = password_hash
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()

        raise UserAlreadyExistsError


    return UserResponse.model_validate(user)

def get_user(db: Session, user_id: int) -> UserResponse:
    user = db.scalar(
        select(User).where(
            User.id == user_id
        )
    )

    if user is None:
        raise UserNotFoundError

    return UserResponse.model_validate(user)

def get_users(db: Session) -> list[UserResponse]:
    users = db.scalars(
        select(User).order_by(User.id)
    ).all()

    return [UserResponse.model_validate(user) for user in users]

def update_user(db: Session, user_id: int, data: UserUpdate) -> UserResponse:
    user = db.scalar(
        select(User).where(
            User.id == user_id
        )
    )

    if user is None:
        raise UserNotFoundError

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return UserResponse.model_validate(user)

def delete_user(db: Session, user_id: int) -> UserResponse:
    user = db.scalar(
        select(User).where(
            User.id == user_id
        )
    )

    if user is None:
        raise UserNotFoundError

    response = UserResponse.model_validate(user)

    db.delete(user)
    db.commit()

    return response

def update_user_role(db: Session, user_id: int, data: UserRolesUpdate) -> UserResponse:
    user = db.scalar(
        select(User).where(
            User.id == user_id
        )
    )

    if user is None:
        raise UserNotFoundError

    roles = db.scalars(
        select(Role).where(
            Role.id.in_(data.roles_ids)
        )
    ).all()

    if len(roles) != len(data.roles_ids):
        raise ValueError('...')

    try:
        user.roles = roles

        db.commit()
        db.refresh(user)

    except Exception as e:
        db.rollback()
        raise

    return UserResponse.model_validate(user)