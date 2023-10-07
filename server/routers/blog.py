from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from database import schemas

from dependencies import get_db

router = APIRouter()


@router.post("/initialize", response_model=schemas.Blog)
async def initialize_blog(blog_info: schemas.BlogCreate, db: Session = Depends(get_db)):
    # global __IS_BLOG_INITIALIZE
    if crud.get_blog_info(db=db):
        raise HTTPException(status_code=400, detail="Blog already been initialized")
    db_blog = crud.initialize_blog(db=db, blog_body=blog_info)
    if isinstance(db_blog, HTTPException):
        raise db_blog
    return db_blog


@router.get("/", response_model=schemas.BlogMeta)
async def get_blog_info(db: Session = Depends(get_db)):
    db_blog_info = crud.get_blog_info(db=db)
    if not db_blog_info:
        raise HTTPException(status_code=400, detail="Blog not initialize yet")
    return db_blog_info
