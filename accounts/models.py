from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    IsArtist = models.BooleanField(default=True)
    ConfirmUser = models.BooleanField(default=False)

    def __str__(self):
        return self.email