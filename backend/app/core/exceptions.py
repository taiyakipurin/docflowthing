class AppException(Exception):
    pass

#users
class UserNotFoundError(AppException):
    pass
class UserAlreadyExistsError(AppException):
    pass
class RoleNotFoundError(AppException):
    pass
class InactiveUserError(AppException):
    pass

#auth
class InvalidCredentialsError(AppException):
    pass
class InvalidRefreshTokenError(AppException):
    pass

#documents
class DocumentNotFoundError(AppException):
    pass
class DocumentAlreadyExistsError(AppException):
    pass
class DocumentStateError(AppException):
    pass
class DocumentAccessDeniedError(AppException):
    pass

#servers
class ServerNotFoundError(AppException):
    pass
class ServerAccessDeniedError(AppException):
    pass

#scenarios
class ScenarioNotFoundError(AppException):
    pass
class ScenarioStateError(AppException):
    pass

#automation jobs
class JobNotFoundError(AppException):
    pass
class JobStateError(AppException):
    pass
class JobAccessDeniedError(AppException):
    pass
