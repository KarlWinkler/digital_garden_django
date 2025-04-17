from django.shortcuts import render, get_object_or_404

from ninja import Router
from ninja.security import django_auth

from post.models import Category, Post, Comment
from post.schemas import (
    PostSchema,
    PostCreateSchema,
    PostUpdateSchema,
    CategorySchema,
    CommentSchema,
    CommentCreateSchema,
    CommentUpdateSchema,
)

from common_schemas import Error


router = Router()


@router.get("/", response={200: list[CategorySchema]})
def list_posts(request):
    return 200, Category.objects.all().select_related()


@router.get("/{id}", response={200: PostSchema})
def get_post(request, id: int):
    return 200, get_object_or_404(Post, pk=id)


@router.post("/", response={201: PostSchema}, auth=django_auth)
def create_post(request, data: PostCreateSchema):
    post = Post.objects.create(**data.dict(exclude_unset=True))

    return 201, post


@router.put("/{id}", response={200: PostSchema, 404: str}, auth=django_auth)
def update_post(request, id: int, data: PostUpdateSchema):
    post = Post.all_objects.filter(pk=id)

    if post.exists():
        post.update(**data.dict(exclude_unset=True))

        return 200, post.first()
    else:
        return 404, "Not Found"


@router.delete("/{id}", response={200: str, 404: str}, auth=django_auth)
def delete_post(request, id: int):
    post = Post.objects.filter(pk=id)

    if post.exists():
        title = post.first().title
        post.update(archived=True)
        
        return 200, f"post - {title} - archived"
    else:
        return 404, "Not Found"



@router.get("/comment/all", response={200: list[CommentSchema]})
def get_all_comments(request):
    return Comment.objects.all()


@router.get("/{id}/comment", response={200: list[CommentSchema]})
def get_comments(request, id: int):
    return Comment.objects.filter(post_id=id)


@router.post("/{id}/comment", response={201: CommentSchema}, auth=django_auth)
def create_comment(request, id: int, data: CommentCreateSchema):
    comment = Comment.objects.create(**data.dict(exclude_unset=True), post_id=id)

    return 201, comment


@router.put("/comment/{id}", response={200: CommentSchema, 404: str}, auth=django_auth)
def update_comment(request, id: int, data: CommentUpdateSchema):
    comment = Comment.all_objects.filter(pk=id)

    if comment.exists():
        comment.update(**data.dict(exclude_unset=True))

        return 200, comment.first()
    else:
        return 404, "Not Found"


@router.delete("/comment/{id}", response={200: str, 404: str}, auth=django_auth)
def delete_comment(request, id: int):
    comment = Comment.objects.filter(pk=id)

    if comment.exists():
        comment.update(archived=True)

        return 200, f"comment {id} archived"
    else:
        return 404, "Not Found"
