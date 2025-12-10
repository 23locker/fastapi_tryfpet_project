from fastapi import HTTPException, status


class FinFlowException(Exception):
    """Base exception for app"""


class ResourceNotFoundException(FinFlowException):
    """Resource not found"""

    def __init__(self, resourse_type: str, resouce_id):
        self.detail = f"{resourse_type} with id {resouce_id} not found"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class InvalidCredentialsException(FinFlowException):
    """Incorrect credentials"""

    def __init__(self):
        self.detail = "Invalid email or password"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=self.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserAlreadyExistsException(FinFlowException):
    """User already exists"""

    def __init__(self, email: str):
        self.detail = f"User with email {email} already exists"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.detail,
        )


class InsufficientFundsException(FinFlowException):
    """Not enough funds"""

    def __init__(self, available: float, required: float):
        self.detail = (
            f"Insufficient funds. Available: {available}, required: {required}"
        )
        super().__init__(self.detail)

    def to_http_excetion(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail,
        )


class InvalidTransactionException(FinFlowException):
    def __init__(self, reason):
        self.detail = f"Invalid transaction {reason}"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail,
        )
