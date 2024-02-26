
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Activity
from .forms import ActivityCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activity/activity_create.html'
    form_class = ActivityCreationForm
    success_url = reverse_lazy('activity_create')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ActivityCreateView, self).form_valid(form)
    
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

