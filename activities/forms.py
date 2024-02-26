from django import forms
from .models import Activity
from accounts.models import CustomUser

class ActivityCreationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_title', 'value', 'start_time', 'end_time', 'status', 'photos', 'desc',]
        widgets = {
            'photos': forms.ClearableFileInput(attrs={'multiple': True}),
            'start_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
            'end_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        return super(ActivityCreationForm, self).__init__(*args, **kwargs)