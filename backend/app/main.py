from fastapi import FastAPI, APIRouter

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    RoleNotFoundError,
    InvalidCredentialsError
)

from app.core.handlers import (
    user_not_found_handler,
    user_already_exists_handler,
    role_not_found_handler,
    invalid_credentials_handler
)

from app.api.v1.routes import (
    user_router,
    role_router,
    auth_router
)

def create_app():
    app = FastAPI()

    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(RoleNotFoundError, role_not_found_handler)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)

    api_v1 = APIRouter(prefix="/api/v1")

    @app.get('/')
    def root():
        return {'message': 'ハローエブリニャン'}

    api_v1.include_router(user_router)
    api_v1.include_router(role_router)
    api_v1.include_router(auth_router)
    app.include_router(api_v1)

    print('good to go')

    return app