from django import forms
from .models import Activity
from accounts.models import CustomUser

class ActivityCreationForm(forms.ModelForm):
    '''
    This class is to set a form for create activity by artist. 
    it specifies that which fields will be display for 
    artist who want to create an activity.
    '''
    class Meta:
        model = Activity
        fields = ['activity_title', 'value', 'start_time', 'end_time', 'status', 'photos', 'desc',]
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
            'end_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
            'photos': forms.ClearableFileInput(attrs={'multiple': True}), # allow artist to upload multiple photos
        }

    def __init__(self, *args, **kwargs):
        return super(ActivityCreationForm, self).__init__(*args, **kwargs)
    
class ActivityCreationFormByAdmin(forms.ModelForm):
    '''
    This class is to set a form for create activity by admin. 
    it specifies that which fields will be display for 
    admin who want to create an activity.
    '''
    class Meta:
        model = Activity
        fields = ['owner', 'activity_title', 'value', 'start_time', 'end_time', 'status', 'photos', 'desc', 'approved',]
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
            'end_time': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
            'photos': forms.ClearableFileInput(attrs={'multiple': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ActivityCreationFormByAdmin, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = CustomUser.objects.filter(is_artist=True) # admin select between artists.
