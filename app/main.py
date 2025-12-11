from app.core.exceptions import (
    FinFlowException,
    InsufficientFundsException,
    InvalidCredentialsException,
    InvalidTransactionException,
    ResourceNotFoundException,
    UserAlreadyExistsException,
)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import users
from app.config import settings

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# exception handlers
@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request, exc: ResourceNotFoundException):
    return exc.to_http_exception()


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(
    request, exc: InvalidCredentialsException
):
    return exc.to_http_exception()


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(
    request, exc: UserAlreadyExistsException
):
    return exc.to_http_exception()


@app.exception_handler(InsufficientFundsException)
async def insufficient_funds_exception_handler(
    request, exc: InsufficientFundsException
):
    return exc.to_http_exception()


@app.exception_handler(InvalidTransactionException)
async def invalid_transaction_exception_handler(
    request, exc: InvalidTransactionException
):
    return exc.to_http_exception()


# routes
app.include_router(
    users.router,
    prefix=settings.api_v1_prefix,
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
