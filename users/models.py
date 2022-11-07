import uuid

import hashlib
import ipdb
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email: str = ..., password: str = ..., **extra_fields: any):
        username = hashlib.sha256(email.encode("utf-8")).hexdigest()[:30]
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        username = hashlib.sha256(email.encode("utf-8")).hexdigest()[:30]
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    email = models.EmailField(max_length=127, unique=True)
    password = models.CharField(max_length=127, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()
