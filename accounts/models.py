from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()
    IsArtist = models.BooleanField(default=True)
    ConfirmUser = models.BooleanField(default=False)

    def __str__(self):
        return self.email