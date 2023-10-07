from fastapi import APIRouter, HTTPException
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from database import crud
from database import schemas

from dependencies import get_db, is_admin
from config import Service, ExceptionLib

router = APIRouter()


@router.post("/create", response_model=schemas.Visitor)
def create_visitor(
    request: Request, visitor: schemas.VisitorCreate, db: Session = Depends(get_db)
):
    hash_info = Service.hash_visitor_inf(request=request)
    db_visitor = crud.create_visitor(db=db, visitor=visitor, hash_info=hash_info)
    if isinstance(db_visitor, ExceptionLib):
        raise db_visitor

    return db_visitor


@router.get(
    "/{visitor_id}", response_model=schemas.Visitor, dependencies=[Depends(is_admin)]
)
def get_visitor(visitor_id: int, db: Session = Depends(get_db)):
    db_visitor = crud.get_visitor(db=db, visitor_id=visitor_id)
    if not db_visitor:
        raise HTTPException(status_code=404, detail=f"no such visitor id: {visitor_id}")

    return db_visitor


@router.get("/", response_model=schemas.Visitor)
def get_current_visitor(request: Request, db: Session = Depends(get_db)):
    visitor_key = Service.hash_visitor_inf(request=request)

    db_visitor = crud.get_visitor_by_hashed_info(db, visitor_key)

    if not db_visitor:
        raise HTTPException(status_code=404)

    return db_visitor
