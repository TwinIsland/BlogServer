from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# tag model and class implement
class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class TagCreate(TagBase):
    pass


class VisitorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str
    email: str
    url: Optional[str] = None


class VisitorCreate(VisitorBase):
    pass


# post model and class implement
class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    cover_url: Optional[str] = None
    is_page: Optional[bool] = False


class PostCreate(PostBase):
    description: Optional[str] = None
    pass


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str


class CommentCreate(CommentBase):
    visitor_key: Optional[str] = None
    article_id: int


# admin model and class implement
class BlogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blog_name: str
    blog_description: str
    admin_name: str
    admin_username: str
    admin_email: str


class BlogCreate(BlogBase):
    admin_password: str


class MediaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_local: bool
    size: Optional[int] = None
    name: Optional[str] = None
    remote_url: Optional[str] = None


class MediaCreate(MediaBase):
    pass


class Visitor(VisitorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_banned: bool
    hashed_info: str
    create_time: datetime
    last_active_time: datetime
    comments: list[CommentBase]


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    by_admin: bool
    owner: "PostMeta"
    author: Optional[VisitorBase]


class Media(MediaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner: "PostLabel"
    create_time: datetime


class Blog(BlogBase):
    model_config = ConfigDict(from_attributes=True)

    create_time: datetime
    admin_avatar: str
    version: str


class Tag(TagBase):
    model_config = ConfigDict()

    id: int
    owners: list["PostLabel"]


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word_count: int
    description: str
    renderer: Optional[str] = None
    tags: list["TagMeta"]
    comments: list[CommentBase]
    medias: list[MediaBase]
    create_time: datetime
    last_active_time: datetime


class TagMeta(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PostMeta(BaseModel):
    id: int
    title: str
    cover_url: Optional[str] = None
    description: Optional[str] = None
    is_page: bool
    word_count: int


class PostLabel(BaseModel):
    id: int
    title: str


class BlogMeta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blog_name: str
    blog_description: str
    admin_name: str
    create_time: datetime
    admin_avatar: str
    version: str


class PostBody(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: list[TagMeta]


Post.model_rebuild()
Tag.model_rebuild()
Comment.model_rebuild()
Media.model_rebuild()


class VisitorUpdate(BaseModel):
    is_banned: bool


class StandardResponse(BaseModel):
    status: Optional[bool] = True
    msg: Optional[str] = ""
    data: BaseModel
