<<<<<<< HEAD

=======
>>>>>>> development
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.CharField(max_length=127, unique=True, null=False)
    password = models.CharField(max_length=127, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField()

    REQUIRED_FIELDS = [
        'email',
        'password'
        ]
    
