from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, unique=True)