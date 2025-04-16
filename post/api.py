from django.shortcuts import render, get_object_or_404

from ninja import Router
from ninja.security import django_auth

from post.models import Category, Post, Comment
from post.schemas import (
    PostSchema,
    PostCreateSchema,
    CategorySchema,
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
    post = Post.objects.create(**data.dict())

    return 201, post


@router.put("/{id}", response={200: PostSchema}, auth=django_auth)
def update_post(request, id: int, data: PostCreateSchema):
    post = Post.objects.filter(pk=id)

    if post.exists():
        post.update(data)

        return 200, post
    else:
        return 404
   
