from typing import Any
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render


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

