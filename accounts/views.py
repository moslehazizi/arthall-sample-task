from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

'''
This is the class based view for signup users that inheriting from 'CreateView' generic class.
'''

class SignupPageView(CreateView):
    form_class = CustomUserCreationForm # Set signup form that we create at (accounts/forms.py)
    success_url = reverse_lazy('login') # Redirect page that comes after user create successfuly.
    template_name = 'registration/signup.html'