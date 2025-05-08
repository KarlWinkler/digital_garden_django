from ninja import Schema
from typing import Optional


class UserCredentials(Schema):
    email: str
    password: str


class GroupSchema(Schema):
    name: str


class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    groups: list[GroupSchema]


class UserCreateSchema(Schema):
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    password: str


class UserUpdateSchema(Schema):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None