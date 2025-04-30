from django.db import models

from post.managers import ArchiveManager


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class StatusChoices(models.TextChoices):
    SEED = "0", "Seed"
    SPROUT = "1", "Sprout"
    FLOWER = "2", "Flower"


class Post(models.Model):
    objects = ArchiveManager()
    all_objects = models.Manager()

    content = models.TextField()
    title = models.TextField()
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=6, choices=StatusChoices, default=StatusChoices.SEED)
    summary = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey('post.Category', on_delete=models.PROTECT, related_name="posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    objects = ArchiveManager()
    all_objects = models.Manager()

    content = models.TextField()
    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # PROTECT to encourage archive rather than delete as the default fuctionality.
    user = models.ForeignKey('user_auth.User', on_delete=models.PROTECT, related_name="comments")
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT, related_name="comments")
    # parent == null then top level comment
    parent = models.ForeignKey('post.Comment', on_delete=models.PROTECT, blank=True, null=True, related_name="children")

    class Meta:
        ordering = ["-created_at"]