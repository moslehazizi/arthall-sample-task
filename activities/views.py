
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
    '''
    This class is inheriting from CreateView generic class and
    it is for creating an activity by artist.
    '''
    model = Activity
    template_name = 'activity/activity_create.html'
    form_class = ActivityCreationForm
    success_url = reverse_lazy('success')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for artist, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not admin user
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.is_artist and request.user.confirm_user) or not request.user.confirm_user:
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        '''
        This is one of 'CreateView''s methods. When a form is submitted and all the data passes validation,
        the 'form_valid' method is called. This method is responsible for what happens next. I use it for 
        set mail sending and sms sender services, So that when instance of model created, Email sender service
        send an email to artist who create activity or admin create activity for him/her. and also sms provide service
        send message via artist's phone number to notify him/her.
        '''
        form.instance.owner = self.request.user
        form.instance.save()

        '''
        I use django built-in mail sender package. So when an instance of Activity is created.
        email sender send an email to console with name of activity owner(artist). I set the email sender
        configuration variable to file system output:

            Line 159 in (settings.py) => EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        
        If you want to use application in production environment, You should change setting to send email using an SMTP server.
        '''
        subject = 'New activity created'
        message = f'Hello dear {self.request.user.username},\n\n You have created new activity with title of {form.instance.activity_title}.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [self.request.user.email]
        send_mail(subject, message, sender_email, recipient_list)

        '''
        The following code is for set kavenegar sms provider service, This is sample and if You want to use it in production environment
        you should create an account in kavenegar website and get an api key, so replace that key with 'api_key' variable.
        '''

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
    '''
    This class is inheriting from CreateView generic class and
    it is for creating an activity by admin for artists.
    '''
    model = Activity
    template_name = 'activity/activity_create_by_admin.html'
    form_class = ActivityCreationFormByAdmin
    success_url = reverse_lazy('success')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''
        This is one of 'CreateView''s methods. When a form is submitted and all the data passes validation,
        the 'form_valid' method is called. This method is responsible for what happens next. I use it for 
        set mail sending and sms sender services, So that when instance of model created, Email sender service
        send an email to artist who create activity or admin create activity for him/her. and also sms provide service
        send message via artist's phone number to notify him/her.
        '''
        form.instance.save()

        '''
        I use django built-in mail sender package. So when an instance of Activity is created.
        email sender send an email to console with name of activity owner(artist). I set the email sender
        configuration variable to file system output:

            Line 159 in (settings.py) => EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        
        If you want to use application in production environment, You should change setting to send email using an SMTP server.
        '''
        subject = 'New activity created'
        message = f'Hello dear {form.instance.owner},\n\n A new activity with title of {form.instance.activity_title} created for you by admin@arthallsample.com for you.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [form.instance.owner.email]
        send_mail(subject, message, sender_email, recipient_list)

        '''
        The following code is for set kavenegar sms provider service, This is sample and if You want to use it in production environment
        you should create an account in kavenegar website and get an api key, so replace that key with 'api_key' variable.
        '''

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
    '''
    This class is inheriting from 'ListView' generic class and it is for
    artist so can see the list of his/her activities that approved by admin
    or those actvities that no need to admin approbation.
    '''
    model = Activity
    template_name = 'activity/activity_list.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for artist, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not admin user
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (not request.user.is_artist and request.user.confirm_user) or not request.user.confirm_user:
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''
        This method is to return activity items that I want to show in template. I use django orm
        to select exact items that proper here => list of artist activities that approved by admin
        or no need to approbation So I filter all activities with owner of request artist that have
        following conditions:
            => (approved=False and activity_title_id__need_to_approve=False) or (approved=True)
        '''
        querySet = [
            Activity.objects.filter(owner=self.request.user, approved=False).filter(activity_title_id__need_to_approve=False),
            Activity.objects.filter(owner=self.request.user, approved=True),
        ]
        return querySet
    
    def get_context_data(self, **kwargs):
        '''
        This method is for change name on list that return from 'get_queryset()',
        I change name of the list from 'object_list' to 'activities',
        So that I use this name in template. It is easier to understand.
        '''
        context = super().get_context_data(**kwargs)
        context['activities'] = context['object_list']
        del context['object_list']
        return context
    
class ActivityListNotApprovedView(LoginRequiredMixin, ListView):
    '''
    This class is inheriting from 'ListView' generic class and it is for
    admin so can see the list of artists activities that not approved yet.
    '''
    model = Activity
    template_name = 'activity/activity_list_not_approved.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''
        This method is to return activity items that I want to show in template. I use django orm
        to select exact items that proper here => list of artists activities that not approved by admin yet.
        So I filter all activities with following conditions:
            => (approved=False and activity_title_id__need_to_approve=True)
        '''
        querySet = Activity.objects.filter(approved=False).filter(activity_title_id__need_to_approve=True)
        return querySet
    
    def get_context_data(self, **kwargs):
        '''
        This method is for change name on list that return from 'get_queryset()',
        I change name of the list from 'object_list' to 'not_approved_activities',
        So that I use this name in template. It is easier to understand.
        '''
        context = super().get_context_data(**kwargs)
        context['not_approved_activities'] = context['object_list']
        del context['object_list']
        return context
    
class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    '''
    This class is inheriting from 'UpdateView' generic class and it is for
    admin so can update activity status and approve not approved activities
    that artists request for approbation.
    '''
    model = Activity
    template_name = 'activity/activity_update.html'
    fields = '__all__'
    success_url = reverse_lazy('activity_list_not_approved') # admin will go to this url after update activity status succesfully.

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()       
        return super().dispatch(request, *args, **kwargs)

class ActivityListViewForAdmin(LoginRequiredMixin, ListView):
    '''
    This class is inheriting from 'ListView' generic class and it is for
    admin so can see the list of all artists activities.
    '''
    model = Activity
    template_name = 'activity/activity_list_all.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        '''
        This is one of 'LoginRequiredMixin''s methods. I use it to set permission to access this view.
        This view is just for admins, So I limmited it.
        So users that request this view should not have following conditions:
            - not anonymous user (not authenticated user)
            - not artist (confirmed or not)
        '''
        if request.user.is_anonymous:
            return HttpResponseForbidden()
        elif request.user.is_authenticated:
            if (request.user.is_artist and request.user.confirm_user) or (request.user.is_artist and not request.user.confirm_user):
                return HttpResponseForbidden()       
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''
        This method is to return activity items that I want to show in template. I use django orm
        to select exact items that proper here => list of all artists activities. So I select all activities.
        '''
        querySet = Activity.objects.all()
        return querySet
    
    def get_context_data(self, **kwargs):
        '''
        This method is for change name on list that return from 'get_queryset()',
        I change name of the list from 'object_list' to 'activities',
        So that I use this name in template. It is easier to understand.
        '''
        context = super().get_context_data(**kwargs)
        context['activities'] = context['object_list']
        del context['object_list']
        return context
    
class ActivityCreateSuccessView(TemplateView):
    '''
    This class is inheriting from 'TemplateView' generic class and it is for
    admin and artists so can see successful messsage when creating an activity.
    '''
    template_name = 'activity/success.html'
    


