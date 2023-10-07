from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from database import schemas

from dependencies import get_db, is_admin

router = APIRouter()


@router.post("/create", response_model=schemas.Tag, dependencies=[Depends(is_admin)])
async def create_tag(
    tag: schemas.TagCreate, post_id: int | None = None, db: Session = Depends(get_db)
):
    return crud.create_tag(db=db, tag=tag, post_id=post_id)


@router.post("/associate", response_model=schemas.Tag, dependencies=[Depends(is_admin)])
async def associate_tag(tag_id: int, post_id: int, db: Session = Depends(get_db)):
    db_tag = crud.associate_tag(db=db, tag_id=tag_id, post_id=post_id)
    if isinstance(db_tag, HTTPException):
        raise db_tag
    return db_tag


@router.get("/", response_model=list[schemas.Tag])
async def get_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db=db)


@router.post("/{tag_id}", response_model=schemas.Tag)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db=db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(
            status_code=404, detail=f"cannot find tag with id: {tag_id}"
        )
    print(db_tag.owners[0].description)
    return db_tag
