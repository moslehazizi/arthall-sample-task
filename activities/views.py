
from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from .models import Activity
from kavenegar import *
from django.core.mail import send_mail
from .forms import ActivityCreationForm, ActivityCreationFormByAdmin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activity/activity_create.html'
    form_class = ActivityCreationForm
    success_url = reverse_lazy('success')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.is_artist and request.user.confirm_user) or not request.user.confirm_user:
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

        ''' SMS sender codes =>

            owner_phone_number = form.instance.owner.phone_number
            # Kavenegar api_key
            api_key = 'kavenegar_api_key'
            # Initialize Kavenegar api
            api = KavenegarAPI(api_key)
            # Send SMS
            params = {
                'receptor': owner_phone_number,
                'message': 'dear {self.request.user.username}, Your activity with title of {form.instance.activity_title} has been created successfully.',
            }
            response = api.sms_send(params)
            # Print response in log
            print(response)
        '''

        return super(ActivityCreateView, self).form_valid(form)
    
class ActivityCreateViewByAdmin(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activity/activity_create_by_admin.html'
    form_class = ActivityCreationFormByAdmin
    success_url = reverse_lazy('success')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.save()
        subject = 'New activity created'
        message = f'Hello dear {form.instance.owner},\n\n A new activity with title of {form.instance.activity_title} created for you by admin@arthallsample.com for you.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [form.instance.owner.email]
        send_mail(subject, message, sender_email, recipient_list)

        ''' SMS sender codes => 

        owner_phone_number = form.instance.owner.phone_number
        # Kavenegar api_key
        api_key = 'kavenegar_api_key'
        # Initialize Kavenegar api
        api = KavenegarAPI(api_key)
        # Send SMS
        params = {
            'receptor': owner_phone_number,
            'message': 'dear {form.instance.owner.username}, An activity with title of {form.instance.activity_title} has been created for you by admin@arthallsample.com successfully.',
        }
        response = api.sms_send(params)
        # Print response in log
        print(response)

        '''

        return super(ActivityCreateViewByAdmin, self).form_valid(form)

class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.is_artist and request.user.confirm_user) or not request.user.confirm_user:
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
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
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
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()       
        return super().dispatch(request, *args, **kwargs)

class ActivityListViewForAdmin(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list_all.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
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
    
class ActivityCreateSuccessView(TemplateView):
    template_name = 'activity/success.html'
    


