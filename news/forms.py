from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment",]
        widgets = {
            "comment": forms.Textarea(attrs={"rows":4})
        }
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders to comment form and remove label
        """        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False
            self.fields[field].widget.attrs["placeholder"] = "Write your comment here"