
from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Activity
from accounts.models import CustomUser
from django.core.mail import send_mail
from .forms import ActivityCreationForm, ActivityCreationFormByAdmin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activity/activity_create.html'
    form_class = ActivityCreationForm
    success_url = reverse_lazy('activity_create')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.IsArtist and request.user.ConfirmUser) or not request.user.ConfirmUser:
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.save()

        subject = 'New activity created'
        message = f'Hello dear {self.request.user.username},\n\n You have created new activity with title of {form.instance.activity_title}.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [self.request.user.email]

        send_mail(subject, message, sender_email, recipient_list)

        return super(ActivityCreateView, self).form_valid(form)
    
class ActivityCreateViewByAdmin(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activity/activity_create_by_admin.html'
    form_class = ActivityCreationFormByAdmin
    success_url = reverse_lazy('activity_create_by_admin')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.IsArtist and request.user.ConfirmUser) or (request.user.IsArtist and not request.user.ConfirmUser):
                return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.save()
        subject = 'New activity created'
        message = f'Hello dear {form.instance.owner},\n\n A new activity with title of {form.instance.activity_title} created for you by admin@arthallsample.com for you.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [form.instance.owner.email]

        send_mail(subject, message, sender_email, recipient_list)
        return super(ActivityCreateViewByAdmin, self).form_valid(form)

class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.IsArtist and request.user.ConfirmUser) or not request.user.ConfirmUser:
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        querySet = [
            Activity.objects.filter(owner=self.request.user, aproved=False).filter(activity_title_id__need_to_aprove=False),
            Activity.objects.filter(owner=self.request.user, aproved=True),
        ]
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = context['object_list']
        del context['object_list']
        return context
    
class ActivityListNotAprovedView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list_not_aproved.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.IsArtist and request.user.ConfirmUser) or (request.user.IsArtist and not request.user.ConfirmUser):
                return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        querySet = Activity.objects.filter(aproved=False).filter(activity_title_id__need_to_aprove=True)
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_aproved_activities'] = context['object_list']
        del context['object_list']
        return context
    
class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    template_name = 'activity/activity_update.html'
    fields = '__all__'
    success_url = reverse_lazy('activity_list_not_aproved')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.IsArtist and request.user.ConfirmUser) or (request.user.IsArtist and not request.user.ConfirmUser):
                return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)

class ActivityListViewForAdmin(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list_all.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.IsArtist and request.user.ConfirmUser) or (request.user.IsArtist and not request.user.ConfirmUser):
                return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        querySet = Activity.objects.all()
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = context['object_list']
        del context['object_list']
        return context
    


