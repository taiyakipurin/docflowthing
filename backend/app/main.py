from fastapi import FastAPI, APIRouter

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

from app.core.handlers import (
    user_not_found_handler,
    user_already_exists_handler,
    role_not_found_handler,
    invalid_credentials_handler,
    invalid_refresh_token_handler,
    document_not_found_handler,
    document_already_exists_handler,
    document_state_error_handler,
    document_access_denied_error_handler
)

from app.api.v1.routes import (
    user_router,
    role_router,
    auth_router,
    doc_router
)

def create_app():
    app = FastAPI()

    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(RoleNotFoundError, role_not_found_handler)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
    app.add_exception_handler(InvalidRefreshTokenError, invalid_refresh_token_handler)
    app.add_exception_handler(DocumentNotFoundError, document_not_found_handler)
    app.add_exception_handler(DocumentAlreadyExistsError, document_already_exists_handler)
    app.add_exception_handler(DocumentStateError, document_state_error_handler)
    app.add_exception_handler(DocumentAccessDeniedError, document_access_denied_error_handler)

    api_v1 = APIRouter(prefix="/api/v1")

    @app.get('/')
    def root():
        return {'message': 'ハローエブリニャン'}

    api_v1.include_router(user_router)
    api_v1.include_router(role_router)
    api_v1.include_router(auth_router)
    api_v1.include_router(doc_router)
    app.include_router(api_v1)

    return app