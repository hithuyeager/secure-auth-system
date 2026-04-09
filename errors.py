class AppError(Exception):
    def __init__(self,message: str,status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UserNotFoundError(AppError):
    super().__init__("USER NOT FOUND", 404)

class WrongPasswordError(AppError):
    super().__init__("WRONG PASSWORD",400)

class UserAlreadyExistError(AppError):
    super().__init__("USER ALREADY EXIST",400)
