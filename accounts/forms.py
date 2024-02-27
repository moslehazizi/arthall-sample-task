from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(SignupForm):
    '''
    I define this class inheriting from 'SignupForm' that is built-in form of 'django-allauth' package
    to extend that form and customize it to signup user, so that have extra fields in signup form.
    '''
    phone_number = PhoneNumberField(label='phone number')
    is_artist = forms.BooleanField(label='Are you an artist:')
    
    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.save()
        return user

class CustomUserCreationFormAdmin(UserCreationForm):
    '''
    This class is inheriting from 'UserCreationForm' to customize django built-in form to create user in django admin site.
    '''
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    '''
    This class is similar to above class and it is for custimize django built-in form to change/update user information in django admin site.
    '''
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')