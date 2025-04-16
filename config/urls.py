from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/user/", "user_auth.api.router")
api.add_router("/post/", "post.api.router")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
