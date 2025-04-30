from django.shortcuts import render, get_object_or_404
from django.db.utils import IntegrityError

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
from post.services import PostService

from common_schemas import Error


router = Router()


@router.get("/", response={200: list[CategorySchema]})
def list_posts(request):
    return 200, Category.objects.all().select_related()


@router.get("/{key}", response={200: PostSchema})
def get_post(request, key: str):
    return 200, get_object_or_404(Post, slug=key)


@router.post("/", response={201: PostSchema, 400: str, 401: str}, auth=django_auth)
def create_post(request, data: PostCreateSchema):
    if not data.slug and not data.title:
        return 401, "Slug or Title must not be blank"
    elif not data.slug:
        data.slug = PostService.slugify(data.title)

    data.category, _ = Category.objects.get_or_create(name=data.category)

    post = Post.objects.filter(slug=data.slug)
    if post.exists():
        return 400, "Slug already exists"
    else:
        post = Post.objects.create(**data.dict(exclude_unset=True))

        return 201, post


@router.put("/{key}", response={200: PostSchema, 404: str, 400: str}, auth=django_auth)
def update_post(request, key: int, data: PostUpdateSchema):
    post = Post.all_objects.filter(pk=key)

    if post.exists():
        try:
            post.update(**data.dict(exclude_unset=True))
            post.first().save(update_fields=['updated_at']) # to update updated_at field

            return 200, post.first()
        except IntegrityError:
            return 400, "Slug already exists"
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


@router.get("/{slug}/comment", response={200: list[CommentSchema]})
def get_comments(request, slug: str):
    return Comment.objects.filter(post__slug=slug)


@router.post("/{slug}/comment", response={201: CommentSchema}, auth=django_auth)
def create_comment(request, slug: str, data: CommentCreateSchema):
    post = get_object_or_404(Post, slug=slug)
    comment = Comment.objects.create(**data.dict(exclude_unset=True), post=post, user=request.user)

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
