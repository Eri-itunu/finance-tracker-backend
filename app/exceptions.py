
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserAlreadyExistsException(AppException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email {email} already exists",
            status_code=400
        )

class DatabaseException(AppException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message=message, status_code=500)

class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401)