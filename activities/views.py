
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

    def form_valid(self, form):
        form.instance.save()
        subject = 'New activity created'
        message = f'Hello dear {form.instance.owner},\n\n A new activity with title of {form.instance.activity_title} created for you by admin@arthallsample.com for you.'
        sender_email = 'admin@arthallsample.com'
        recipient_list = [form.instance.owner.email]

        send_mail(subject, message, sender_email, recipient_list)
        return super(ActivityCreateViewByAdmin, self).form_valid(form)
    
    
class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activity/activity_detail.html'

class ActivityListView(ListView):
    model = Activity
    template_name = 'activity/activity_list.html'

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

class ActivityListViewForAdmin(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list_all.html'
    
    def get_queryset(self):
        querySet = Activity.objects.all()
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = context['object_list']
        del context['object_list']
        return context
    


