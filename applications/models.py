from uuid import uuid4

from django.db import models


class Application(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="applications"
    )

    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="applications"
    )
