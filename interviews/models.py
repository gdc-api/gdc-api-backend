import uuid

from django.db import models


class Interview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    schedule = models.DateTimeField()
    location = models.TextField(blank=True)
    was_aprooved = models.BooleanField(blank=True, default=False)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    def toogle_was_approved(self):
        self.was_aprooved = not self.was_aprooved

    ...
