from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationFormAdmin, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFormAdmin
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'IsArtist', 'ConfirmUser',]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number", "IsArtist", "ConfirmUser",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "phone_number", "IsArtist", "ConfirmUser",)}),)

admin.site.register(CustomUser, CustomUserAdmin)