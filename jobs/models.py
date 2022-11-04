import uuid
from django.db import models


class Level(models.TextChoices):
    INTERN = "Estágio"
    TRAINEE = "Treinee"
    JUNIOR = "Júnior"
    MID = "Pleno"
    SENIOR = "Sênior"
    DEFAULT = "Não definido"
    ...


class Category(models.TextChoices):
    FRONT = "Front-End"
    BACK = "Back-End"
    FULL = "Full-Stack"
    DEFAULT = "Não definido"
    ...


class Job(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    url = models.CharField(max_length=254, unique=True)
    title = models.CharField(max_length=127)
    period = models.CharField(max_length=15)
    location = models.CharField(max_length=30)
    contract = models.CharField(max_length=15)
    estimated_pay = models.PositiveIntegerField()

    level = models.CharField(
        max_length=15,
        choices=Level.choices,
        default=Level.DEFAULT,
    )

    category = models.CharField(
        max_length=15,
        choices=Category.choices,
        default=Category.DEFAULT,
    )

<<<<<<< Updated upstream
    comapany = models.ForeignKey(
=======
    company = models.ForeignKey(
>>>>>>> Stashed changes
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    ...
