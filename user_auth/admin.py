from django.contrib import admin
from user_auth.models import User

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)