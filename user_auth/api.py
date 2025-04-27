from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

from ninja import Router
from ninja.security import django_auth

from user_auth.models import User
from user_auth.schemas import UserSchema, UserCredentials, SignupSchema

from common_schemas import Error


router = Router(auth=django_auth)

@router.get("/self", response={200: UserSchema, 404: str})
def get_current_user(request):
    if request.user.is_authenticated:
        return 200, request.user
    else:
        return 404, "User not authenticated"


@router.get("/", response={200: list[UserSchema]})
def list_users(request):
    return User.objects.all()


@router.get("/{id}", response={200: UserSchema}) 
def get_user(request, id: int):
    return get_object_or_404(User, pk=id)


@router.post("/auth/login", response={200: UserSchema, 401: Error}, auth=None)
def login(request: HttpRequest, response: HttpResponse, credentials: UserCredentials):
    user = authenticate(request, email=credentials.email, password=credentials.password)

    if user is not None:
        auth_login(request, user)
        response.set_cookie("cookie", "test", samesite='Lax', secure=True)
        return 200, user
    else:
        return 401, {'message': 'Invalid Username or Password'}


@router.post("/auth/signup", response={422: Error, 201: UserSchema})
def signup(request, signup: SignupSchema):
    try:
        user = User.objects.create(signup)
        user.set_password(signup.password)
        user.save()

        return 201, user
    except:
        return 401, {'message': 'Error creating user'}


@router.post("/auth/logout")
def logout(request):
    auth_logout(request)
    return 200, {'message': 'Logged out'}
