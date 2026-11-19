from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    DocumentStateError,
    DocumentAccessDeniedError
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

async def invalid_refresh_token_handler(
        request: Request,
        exc: InvalidRefreshTokenError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Invalid refresh token'}
    )

async def document_not_found_handler(
        request: Request,
        exc: DocumentNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={'detail': 'Document not found'}
    )

async def document_already_exists_handler(
        request: Request,
        exc: DocumentAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={'detail': 'Document already exists'}
    )

async def document_state_error_handler(
        request: Request,
        exc: DocumentStateError
):
    return JSONResponse(
        status_code=400,
        content={'detail': 'Document state error'}
    )

async def document_access_denied_error_handler(
        request: Request,
        exc: DocumentAccessDeniedError
):
    return JSONResponse(
        status_code=401,
        content={'detail': 'Document access denied'}
    )

