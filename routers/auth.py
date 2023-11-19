from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from database import crud
import asyncio

from config import (
    Service,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    LOGIN_TIME_DELAY_SECOND,
)
from dependencies import get_db
from pydantic import BaseModel

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/", response_model=Token)
async def log_in(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_blog_info = crud.get_blog_info(db=db)

    if not db_blog_info:
        raise HTTPException(status_code=400, detail="Blog not initialize yet")

    if not (
        db_blog_info.admin_username == form_data.username
        and Service.check_password(
            password=form_data.password,
            hashed_password=db_blog_info.admin_hashed_password,
        )
    ):
        # delay if username not match due to check password consume more time
        if db_blog_info.admin_username != form_data.username:
            await asyncio.sleep(LOGIN_TIME_DELAY_SECOND)

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": db_blog_info.admin_username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
