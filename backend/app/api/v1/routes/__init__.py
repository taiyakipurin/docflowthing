from .users import router as user_router
from .roles import router as role_router
from .auth import router as auth_router

__all__ = [
    'user_router',
    'role_router',
    'auth_router'
]