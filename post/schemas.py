from ninja import Schema
import datetime


class PostSchema(Schema):
    id: int
    title: str
    status: str
    summary: str
    slug: str
    content: str
    created_at: datetime.date
    updated_at: datetime.date


class PostCreateSchema(Schema):
    title: str
    status: str
    summary: str
    slug: str
    content: str
    category_id: int


class CategorySchema(Schema):
    name: str
    posts: list[PostSchema]
