from django.db import models

from authentication.models import MainModel

# Create your models here.


class Contact(MainModel, models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email
