from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.TextField()

    class Meta:
        permissions = [("app_admin", "App adminitration permission")]
