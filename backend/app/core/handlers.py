from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError
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
