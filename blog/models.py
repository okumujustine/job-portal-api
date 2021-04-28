from django.db import models

from authentication.models import MainModel, CustomUser

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(
        to=CustomUser, related_name='blog_posts', on_delete=models.CASCADE)
