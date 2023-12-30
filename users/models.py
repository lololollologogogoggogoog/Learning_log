from django.db import models


class Users(models.Model):
    ip = models.CharField(max_length=200)
    ban = models.BooleanField(default=False)
