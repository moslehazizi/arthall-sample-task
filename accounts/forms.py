from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(SignupForm):
    phone_number = PhoneNumberField(label='phone number')
    IsArtist = forms.BooleanField(label='Are you an artist:')
    
    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.save()
        return user

class CustomUserCreationFormAdmin(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')