from .users import router as user_router
from .roles import router as role_router
from .auth import router as auth_router
from .docs import router as doc_router
from .server import router as server_router
from .scenario import router as scenario_router

__all__ = [
    'user_router',
    'role_router',
    'auth_router',
    'doc_router',
    'server_router',
    'scenario_router'
]