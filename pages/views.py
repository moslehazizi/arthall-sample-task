from typing import Any
from django.http.response import HttpResponseForbidden
from django.http import HttpRequest
from django.views.generic import TemplateView, UpdateView, ListView
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView): # This is class based view to render home page template file.
    template_name = 'home.html' # Location of home page template file in template folder.
    
    

class RegisterConfirmationView(LoginRequiredMixin, ListView):
    '''
    This class is to return list of artists that not confirmed by admin,
    So that admin can confirm them.
    '''
    model = CustomUser
    template_name = 'pages/register_confirmation.html'
    fields = ('email', 'is_artist', 'confirm_user',)

    def get_queryset(self):
        '''
        This method is to return items that I want to show in template from database.
        I use django orm to select exact items that proper here => not confirmed artists
        So I filter all users that conditions are => 'is_artist=True' and 'confirm_user=False'
        '''
        querySet = CustomUser.objects.filter(confirm_user=False, is_artist=True)
        return querySet
    
    def get_context_data(self, **kwargs):
        '''
        This method is for change name on list that return from 'get_queryset()',
        I change name of the list from 'object_list' to 'not_confirmed_artists',
        So that I use this name in template. It is easier to understand.
        '''
        context = super().get_context_data(**kwargs)
        context['not_confirmed_artists'] = context['object_list']
        del context['object_list']
        return context
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it for set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view must not have bellow conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    '''
    This class is for admin to update artist accounts and confirm their accounts.
    '''
    model = CustomUser
    template_name = 'pages/user_update.html'
    fields = ('email', 'is_artist', 'confirm_user',) # Admin change 'confirm_user' field and check it for each artist that register to website.

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it for set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view must not have bellow conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next')

