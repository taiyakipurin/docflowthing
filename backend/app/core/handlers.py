from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    InvalidCredentialsError
)

async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'User not found'}
    )

async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={'detail': 'User already exists'}
    )

async def role_not_found_handler(
        request: Request,
        exc: RoleNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'Role not found'}
    )

async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Invalid credentials'}
    )