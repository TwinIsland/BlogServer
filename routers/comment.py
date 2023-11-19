from fastapi import APIRouter
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import crud
from database import schemas

from dependencies import get_db
from utils import Utils


router = APIRouter()


@router.post("/post", response_model=schemas.Comment)
def post_comment(
    comment: schemas.CommentCreate, request: Request, db: Session = Depends(get_db)
):
    if Utils.is_admin(request):
        return crud.post_comment(db=db, comment=comment, by_admin=True)

    if comment.visitor_key is None:
        raise HTTPException(status_code=400)

    db_comment = crud.post_comment(db=db, comment=comment)
    if isinstance(db_comment, HTTPException):
        raise db_comment
    return db_comment


@router.get("/", response_model=list[schemas.Comment])
def get_comment_by_post_id(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments(db=db, post_id=post_id)
