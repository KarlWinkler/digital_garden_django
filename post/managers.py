from django.db import models


class ArchiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)