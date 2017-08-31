from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True)
    url = models.URLField(null=True)
    picture_url = models.URLField(null=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
