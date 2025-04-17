from typing import Optional
from ninja import Schema
from datetime import datetime


from user_auth.schemas import UserSchema


class CommentSchema(Schema):
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserSchema


class CommentCreateSchema(Schema):
    content: str
    user_id: int
    archived: int = False


class CommentUpdateSchema(Schema):
    content: str = None
    user_id: int = None
    archived: int = None


class PostSchema(Schema):
    id: int
    title: str
    status: str
    summary: str
    slug: str
    content: str
    created_at: datetime
    updated_at: datetime
    archived: bool


class PostCreateSchema(Schema):
    title: str
    status: str
    summary: str
    slug: str
    content: str
    category_id: int
    archived: bool = None


class PostUpdateSchema(Schema):
    title: str = None
    status: str = None
    summary: str = None
    slug: str = None
    content: str = None
    category_id: int = None
    archived: bool = None

class CategorySchema(Schema):
    name: str
    posts: list[PostSchema]
