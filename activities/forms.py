from django import forms
from .models import Activity

class ActivityCreationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_title', 'value', 'start_time', 'end_time', 'status', 'photos', 'desc',]
        widgets = {
            'photos': forms.ClearableFileInput(attrs={'multiple': True}),
        }
