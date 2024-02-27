from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationFormAdmin, CustomUserChangeForm

CustomUser = get_user_model() 
'''
I defined a model in (accounts/models.py) for store users in database.
Then introduce this model to our django project config in (settings.py)

    in line '146' => AUTH_USER_MODEL = 'accounts.CustomUser'

Know I import that model here to be globaly available in admin file and
have no mistake when I work on main user model in 'admin.py'.
'''


class CustomUserAdmin(UserAdmin):
    '''
    I define a class inheriting from UserAdmin that is the default administration interface
    for managing users in the Django admin site, so that to do some changes in displaying fields and ..
    of user model in django admin site. 
    '''
    add_form = CustomUserCreationFormAdmin # I customized user creation form for admin panel by defining a custom form in (accounts/forms.py) and import it here.
    form = CustomUserChangeForm # I customized user change form for admin panel by defining a custom form in (accounts/forms.py) and import it here.
    model = CustomUser 
    list_display = ['email', 'username', 'phone_number', 'is_artist', 'confirm_user',] # I want to see these fields of user model as columns in the list view of django admin site.
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_artist", "confirm_user",)}),) # I want to see these fields in the django admin interface when managing user accounts.
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "is_artist", "confirm_user",)}),) # I want to customize these fields of user model when adding a new user in django admin site.

admin.site.register(CustomUser, CustomUserAdmin)