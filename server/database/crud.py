import datetime

from sqlalchemy.orm import defer, Session
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from . import models, schemas
from config import (
    Toolkit,
    Service,
    RendererEnum,
    ExceptionLib,
    MAX_OUTPUT_ITEM_NUM,
    SAFETY_STRICT,
    COMMENT_GAP_SECOND,
)


def get_blog_info(db: Session):
    return db.query(models.Blog).first()


def initialize_blog(db: Session, blog_body: schemas.BlogCreate):
    if SAFETY_STRICT:
        if not Toolkit.is_valid_email(blog_body.admin_email):
            return ExceptionLib.EMAIL_NOT_IN_FORMAT

    hashed_password = Service.hash_password(blog_body.admin_password)
    db_blog_info = models.Blog(
        **blog_body.model_dump(exclude={"admin_password"}),
        admin_hashed_password=hashed_password,
        admin_avatar=Service.get_avatar(email=blog_body.admin_email),
    )
    db.add(db_blog_info)
    db.commit()
    db.refresh(db_blog_info)
    return db_blog_info


def add_post(db: Session, post: schemas.PostCreate, renderer: RendererEnum):
    if SAFETY_STRICT:
        if post.cover_url and not Toolkit.is_valid_url(post.cover_url):
            raise ExceptionLib.URL_NOT_IN_FORMAT

    db_renderer = None if renderer == RendererEnum.DEFAULT else renderer
    db_post = models.Post(
        **post.model_dump(), word_count=len(post.content), renderer=db_renderer
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_tags(db: Session, limit: int = MAX_OUTPUT_ITEM_NUM):
    return db.query(models.Tag).limit(limit).all()


def get_comments(db: Session, post_id: int, limit: int = MAX_OUTPUT_ITEM_NUM):
    return (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == post_id)
        .limit(limit)
        .all()
    )


def post_comment(db: Session, comment: schemas.CommentCreate, by_admin: bool = False):
    db_owner = get_post(db, comment.article_id)
    if not db_owner:
        raise HTTPException(
            status_code=400, detail=f"no such post: {comment.article_id}"
        )

    if by_admin:
        db_author = None
    else:
        db_author = get_visitor_by_hashed_info(comment.visitor_key)

        if not db_author:
            return HTTPException(
                status_code=400,
                detail=f"no such visitor with hash: {comment.visitor_key}",
            )

        comment_gap_second = datetime.datetime.now() - db_author.last_active_time
        wait_time_str = "{:.1f}".format(
            COMMENT_GAP_SECOND - comment_gap_second.total_seconds()
        )
        if comment_gap_second.total_seconds() < COMMENT_GAP_SECOND and len(
            db_author.comments
        ):
            return HTTPException(
                status_code=400,
                detail=f"post comment to frequent, try post after {wait_time_str} second",
            )

        db_author.last_active_time = datetime.datetime.now()
        db.add(db_author)

    db_comment = models.Comment(
        **comment.model_dump(exclude={"author_key", "article_id"}),
        owner=db_owner,
        author=db_author,
        by_admin=by_admin,
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_post_metas(
    db: Session, post_id: int | None = None, limit: int = MAX_OUTPUT_ITEM_NUM
):
    """

    :param post_id: the id for post, return all if not given
    :param db: database session
    :param limit: limit output
    :return: post id and post title
    """
    if post_id:
        db_post_meta = (
            db.query(models.Post).options(defer(models.Post.content)).get(post_id)
        )
        if not db_post_meta:
            return HTTPException(
                status_code=404,
                detail=f"Post: aid{post_id} not found in the database.",
            )
        else:
            return [db_post_meta]
    return db.query(models.Post).options(defer(models.Post.content)).limit(limit).all()


def get_post(db: Session, post_id: int):
    """

    :param post_id: the id for post
    :param db: database session
    :return: the whole post body with given id
    """
    return db.query(models.Post).get(post_id)


def create_tag(db: Session, tag: schemas.TagCreate, post_id: int | None = None):
    """

    :param post_id: associate with given post id, not associate if not given
    :param db: database session
    :param tag: tag to be created
    :return: the session instance
    """
    try:
        db_tag = models.Tag(**tag.model_dump())

        if post_id:
            db_tag.owners.append(get_post(db=db, post_id=post_id))

        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Tag with the same name already exists"
        )


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).get(tag_id)


def associate_tag(db: Session, tag_id: int, post_id: int):
    try:
        # Check if both post and tag exist in the database
        db_post = db.query(models.Post).get(post_id)
        db_tag = db.query(models.Tag).get(tag_id)

        if not db_post or not db_tag:
            return HTTPException(
                status_code=404, detail="Post or Tag not found in the database."
            )

        # Check if the association already exists
        if db_post in db_tag.owners:
            return db_tag

        # Create the association between the tag and post
        db_tag.owners.append(db_post)
        db.commit()

        # Refresh the db_tag to get the updated version with the new association
        db.refresh(db_tag)
        return db_tag

    except (NoResultFound, ExceptionLib) as e:
        # Instead of raising exceptions, we raise an HTTPException with the error message
        # This will be caught by FastAPIs exception handling and returned as a JSON response.
        return HTTPException(status_code=400, detail=str(e))


def get_visitor(db: Session, visitor_id: int):
    """

    :param visitor_id: the id for visitor
    :param db: database session
    :return: the whole post body with given id
    """
    db_visitor = db.query(models.Visitor).get(visitor_id)
    return db_visitor


def get_visitor_by_hashed_info(db: Session, hashed_info: str):
    return (
        db.query(models.Visitor)
        .filter(models.Visitor.hashed_info == hashed_info)
        .first()
    )


def create_visitor(db: Session, visitor: schemas.VisitorCreate, hash_info: str):
    if SAFETY_STRICT:
        if not Toolkit.is_valid_email(visitor.email):
            return ExceptionLib.EMAIL_NOT_IN_FORMAT
        if visitor.url and not Toolkit.is_valid_url(visitor.url):
            return ExceptionLib.URL_NOT_IN_FORMAT

    db_visitor = (
        db.query(models.Visitor).filter(models.Visitor.hashed_info == hash_info).first()
    )
    if db_visitor:
        # do update on current visitor
        db_visitor.user_name = visitor.user_name
        db_visitor.email = visitor.email
        db_visitor.url = visitor.url
    else:
        db_visitor = models.Visitor(**visitor.model_dump(), hashed_info=hash_info)

    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


def update_visitor(db: Session, visitor_id: int, visitor_update: schemas.VisitorUpdate):
    try:
        db_visitor = db.query(models.Visitor).get(visitor_id)

        if not db_visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")

        # Update the fields from the visitor_update payload
        for key, value in visitor_update.model_dump():
            setattr(db_visitor, key, value)

        db.commit()
        db.refresh(db_visitor)
        return db_visitor
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Integrity Error occurred during update"
        )


def add_media(db: Session, media: schemas.MediaCreate, post_id: int):
    db_post = db.query(models.Post).get(post_id)

    if not db_post:
        return HTTPException(status_code=404, detail="Post not found in the database.")

    db_media = models.Media(**media.model_dump(), owner=db_post)

    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media
