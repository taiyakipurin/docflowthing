class AppException(Exception):
    pass

class UserNotFoundError(AppException):
    pass

class UserAlreadyExistsError(AppException):
    pass

class RoleNotFoundError(AppException):
    pass

class InactiveUserError(AppException):
    pass

class InvalidCredentialsError(AppException):
    pass

class InvalidRefreshTokenError(AppException):
    pass

class DocumentNotFoundError(AppException):
    pass

class DocumentAlreadyExistsError(AppException):
    pass

class DocumentStateError(AppException):
    pass

class DocumentAccessDeniedError(AppException):
    pass