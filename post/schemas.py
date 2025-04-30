from typing import Optional
from ninja import Field, Schema
from datetime import datetime


from user_auth.schemas import UserSchema


class CommentSchema(Schema):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserSchema
    children: list['CommentSchema'] = []


class CommentCreateSchema(Schema):
    content: str
    parent_id: int = None
    archived: bool = False


class CommentUpdateSchema(Schema):
    content: str = None
    user_id: int = None
    archived: int = None


class SimpleCategorySchema(Schema):
    name: str


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
    category: SimpleCategorySchema
    top_level_comments: list[CommentSchema]


class PostCreateSchema(Schema):
    title: str
    status: str
    summary: str
    content: str
    category: str
    slug: str = None
    archived: bool = None


class PostUpdateSchema(Schema):
    title: str = None
    status: str = None
    summary: str = None
    slug: str = None
    content: str = None
    category_id: int = None
    archived: bool = None


class SimplePostSchema(Schema):
    title: str
    slug: str
    status: str
    summary: str


class CategorySchema(Schema):
    name: str
    posts: list[SimplePostSchema]
