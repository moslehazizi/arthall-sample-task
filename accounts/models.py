from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

'''
I define a custom user model, It has 3 fields plus other 
built-in fields of 'AbstractUser' such as 'username', 'email' and etc.
Those 3 fields are:
 - phone_number:  To store phone number of users so that send message to them by sms provider service.
 - is_artist:     To check that user is artist or admin.
 - confirm_user:  To check that user is confirmed by admin or not.

I define these fields to prevent create extra model for define the role of each user => admin or artist

This is more simple and optimal, 
So that if user has 'is_artist=True' and 'confirm_user=True' (that default is False and admin change it to True and confirm artist) => user is artist
and if user has 'is_artist=False' and 'confirm_user=True' (superuser in django admin site can create admin user) => user is admin

'''

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()
    is_artist = models.BooleanField(default=True)
    confirm_user = models.BooleanField(default=False)

    def __str__(self):
        return self.email