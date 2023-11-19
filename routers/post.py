from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from config import Renderer, RendererEnum, Service, MAX_OUTPUT_ITEM_NUM

from database import crud
from database import schemas

from dependencies import get_db, is_admin

router = APIRouter()
renderer = Renderer()


def fill_db_post(db_post):
    if db_post.cover_url is None:
        db_post.cover_url = Service.get_default_banner(db_post)
    if not db_post.description:
        db_post.description = Service.get_default_description(db_post)
    if not db_post.renderer:
        db_post.renderer = Renderer.DEFAULT_RENDERER_NAME


@router.post("/post", response_model=schemas.Post, dependencies=[Depends(is_admin)])
async def add_post(
        post: schemas.PostCreate,
        renderer: RendererEnum = RendererEnum.DEFAULT,
        db=Depends(get_db),
):
    if not post.description:
        post.description = Service.generate_description(_post_body=post)

    db_post = crud.add_post(db=db, post=post, renderer=renderer)
    fill_db_post(db_post)
    return db_post


@router.post("/full/{post_id}", response_model=schemas.Post)
async def get_full_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=404, detail=f"cannot find post with id: {post_id}"
        )

    fill_db_post(db_post)
    return crud.get_post(db=db, post_id=post_id)


@router.post("/{post_id}", response_model=schemas.PostBody)
async def get_post_body(
        post_id: int, render: bool = False, db: Session = Depends(get_db)
):
    db_post = crud.get_post(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=404, detail=f"cannot find post with id: {post_id}"
        )

    if not db_post.cover_url:
        db_post.cover_url = Service.get_default_banner(db_post)

    if render:
        use_renderer = (
            Renderer.DEFAULT_RENDERER_NAME if not db_post.renderer else db_post.renderer
        )

        if use_renderer not in renderer.renderers:
            raise HTTPException(
                status_code=500,
                detail=f"renderer: '{use_renderer}' detached from config",
            )
        render_method = renderer.renderers[use_renderer]
        db_post.content = render_method(db_post.content)

    return db_post


@router.get("/", response_model=list[list[schemas.PostMeta]])
async def get_post_meta(
        limit: int | None = None, split: int | None = None, db: Session = Depends(get_db)
):
    limit = MAX_OUTPUT_ITEM_NUM if not limit else limit
    db_post_meta = crud.get_post_metas(db=db, limit=limit)

    for db_post in db_post_meta:
        fill_db_post(db_post)

    if isinstance(db_post_meta, HTTPException):
        raise db_post_meta
    if split and split > 0:
        post_meta_chunk = [
            db_post_meta[i: i + split] for i in range(0, len(db_post_meta), split)
        ]
        return post_meta_chunk
    return [db_post_meta]
