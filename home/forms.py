from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "email", "message",)
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders remove labels
        """        
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Full name',
            'email': 'Email to contact you',
            'message': 'Write you message here',
        }        
        
        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].label = False