import uuid

from django.db import models


class Interview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    schedule = models.DateTimeField()
    location = models.TextField(blank=True)
    was_aprooved = models.BooleanField(blank=True, default=False)

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    ...
