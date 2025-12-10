import re
import uuid

import uvicorn
from config import settings
from fastapi import FastAPI, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ====== create app ======
app = FastAPI(title="FinFlow")

# ===== API ======

user_router = APIRouter()


@user_router.post("/")
async def create_user(self):
    pass


# create the instance for the routes
router = APIRouter()


# set routes to the app instance
router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(router)


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
