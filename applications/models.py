from django.db import models
from jobs.models import Job
from pyexpat import model
from users.models import User

from uuid import uuid4


class Application(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
