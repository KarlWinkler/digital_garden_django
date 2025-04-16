from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField(unique=True)
    preferences = models.TextField(default='')
    username = models.TextField()

    bio = models.TextField(blank=True)