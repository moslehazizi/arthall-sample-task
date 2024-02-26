from django.views.generic import TemplateView, UpdateView, ListView
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = 'home.html'
    
    

class RegisterConfirmationView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'not_confirmed_artists'
    template_name = 'pages/register_confirmation.html'
    fields = ('email', 'IsArtist', 'ConfirmUser',)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'pages/user_update.html'
    fields = ('email', 'IsArtist', 'ConfirmUser',)

    def get_success_url(self):
        return self.request.GET.get('next')

