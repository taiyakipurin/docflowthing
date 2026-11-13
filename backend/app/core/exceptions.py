class AppException(Exception):
    pass

class UserNotFoundError(AppException):
    pass

class UserAlreadyExistsError(AppException):
    pass

class RoleNotFoundError(AppException):
    pass