from fastapi import HTTPException, status


class FinFlowException(Exception):
    """Base exceptions for app"""

    pass


class ResourceNotFoundException(FinFlowException):
    """Resource not found"""

    def __init__(self, resource_type: str, resource_id):
        self.detail = f"{resource_type} with id {resource_id} not found"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.detail,
        )


class InvalidCredentialsException(FinFlowException):
    """Invalid credentials exception"""

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
    """User alreade exists"""

    def __init__(self, email: str):
        self.detail = f"User with email {email} already exists"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.detail,
        )


class InsufficientFundsException(FinFlowException):
    """Insufficient funds"""

    def __init__(self, available: float, required: float):
        self.detail = (
            f"Insufficient funds. Available: {available}, Required: {required}"
        )
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail,
        )


class InvalidTransactionException(FinFlowException):
    """Invalid Transaction"""

    def __init__(self, reason: str):
        self.detail = f"Invalid transaction: {reason}"
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail,
        )
