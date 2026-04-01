from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    CHOICES = (
        (1.0, '1'), (1.25, '1.25'), (1.5, '1.5'), (1.75, '1.75'),
        (2.0, '2'), (2.25, '2.25'), (2.5, '2.5'), (2.75, '2.75'),
        (3.0, '3'), (3.25, '3.25'), (3.5, '3.5'), (3.75, '3.75'),
        (4.0, '4'), (4.25, '4.25'), (4.5, '4.5'), (4.75, '4.75'),
        (5.0, '5')
    )


    rating = forms.ChoiceField(choices = tuple([('', 'Rating (optional)')] + list(CHOICES)), required=False)
    
    
    class Meta:
        model = Review
        fields = ("review", "rating",)