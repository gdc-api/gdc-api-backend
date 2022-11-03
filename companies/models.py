from django.db import models
import uuid


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    segment = models.CharField(max_length=30)
