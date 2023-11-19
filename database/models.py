from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base
from config import VERSION

association_table = Table(
    "relation",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
)


class Blog(Base):
    __tablename__ = "blog"

    # Blog information
    blog_name = Column(String, primary_key=True)
    blog_description = Column(String)

    # Admin information
    admin_name = Column(String)
    admin_username = Column(String)
    admin_email = Column(String)
    admin_avatar = Column(String)
    admin_hashed_password = Column(String)

    # Timestamps
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    # Versioning
    version = Column(String, default=VERSION)


class Visitor(Base):
    __tablename__ = "visitor"

    # Visitor information
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, index=True)
    email = Column(String, index=True)
    url = Column(String, nullable=True, index=True)
    is_banned = Column(Boolean, index=True, default=False)
    hashed_info = Column(String, unique=True, index=True)

    # Relationships
    comments = relationship("Comment", back_populates="author")

    # Timestamps
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    last_active_time = Column(DateTime(timezone=True), server_default=func.now())


class Post(Base):
    __tablename__ = "post"

    # Post information
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    word_count = Column(Integer, index=True)
    cover_url = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True, index=True)
    is_page = Column(Boolean, default=False, index=True)
    renderer = Column(String, nullable=True, index=True)

    # Relationships
    tags = relationship("Tag", back_populates="owners", secondary=association_table)
    comments = relationship("Comment", back_populates="owner")
    medias = relationship("Media", back_populates="owner")

    # Timestamps
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    last_active_time = Column(DateTime(timezone=True), server_default=func.now())


class Media(Base):
    __tablename__ = "media"

    # Media information
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=True)
    size = Column(Integer, index=True, nullable=True)

    # Media storage
    is_local = Column(String, index=True, default=True)
    remote_url = Column(String, index=True, nullable=True)

    # Relationships
    owner_id = Column(Integer, ForeignKey("post.id"), index=True)
    owner = relationship("Post", back_populates="medias")

    # Timestamps
    create_time = Column(DateTime(timezone=True), server_default=func.now())


class Tag(Base):
    __tablename__ = "tag"

    # Tag information
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    # Relationships
    owners = relationship("Post", back_populates="tags", secondary=association_table)


class Comment(Base):
    __tablename__ = "comment"

    # Comment information
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(String, index=True)

    # Relationships
    owner_id = Column(Integer, ForeignKey("post.id"), index=True)
    owner = relationship("Post", back_populates="comments")
    by_admin = Column(Boolean, default=False, index=True)
    author_id = Column(Integer, ForeignKey("visitor.id"), nullable=True, index=True)
    author = relationship("Visitor", back_populates="comments")
