import uuid

from django.db import models


class Interview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    schedule = models.DateTimeField()
    location = models.TextField(blank=True)
    was_aprooved = models.BooleanField(blank=True, default=False)
    passed = models.BooleanField(blank=True, default=False)

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

    def toggle_was_approved(self):
        self.was_aprooved = bool(not self.was_aprooved)
        return self.was_aprooved

    def toggle_passed(self):
        self.passed = bool(not self.passed)
        return self.passed

    ...
