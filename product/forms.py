from django import forms
from .models import Review, Category, Tag, Product


class ReviewForm(forms.ModelForm):
    CHOICES = (
        ('1.00', '1.00'), (1.25, '1.25'), ('1.50', '1.50'), (1.75, '1.75'),
        ('2.00', '2.00'), (2.25, '2.25'), ('2.50', '2.50'), (2.75, '2.75'),
        ('3.00', '3.00'), (3.25, '3.25'), ('3.50', '3.50'), (3.75, '3.75'),
        ('4.00', '4.00'), (4.25, '4.25'), ('4.50', '4.50'), (4.75, '4.75'),
        ('5.00', '5.00')
    )


    rating = forms.ChoiceField(choices = tuple([(0.00, 'Rating (optional)')] + list(CHOICES)), required=False,)
        
    
    class Meta:
        model = Review
        fields = ["review", "rating",]
        widgets = {
            "review": forms.Textarea(attrs={"rows":5})
        }

class ProductFormEdit(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'tag', 'sku', 'price', 'rating', 'image_name']
        
    image = forms.ImageField(label="Image", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #categories = Category.objects.all()
        #cat_friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        #tags = Tag.objects.all()
        #tag_friendly_names = [(t.id, t.get_friendly_name()) for t in tags]

        #self.fields['category'].choices = cat_friendly_names
        #self.fields['tag'].choices = tag_friendly_names
        
        for field_name in ['category', 'tag', 'sku']:
            self.fields[field_name].disabled = True
            self.fields[field_name].required = False
            

class ProductFormAdd(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'tag', 'sku', 'price', 'rating', 'image_name']
        
    image = forms.ImageField(label="Image", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        cat_friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        tags = Tag.objects.all()
        tag_friendly_names = [(t.id, t.get_friendly_name()) for t in tags]

        self.fields['category'].choices = cat_friendly_names
        self.fields['tag'].choices = tag_friendly_names
        self.fields['sku'].disabled = True