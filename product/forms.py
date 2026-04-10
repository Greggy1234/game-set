from django import forms
from .models import Review, Category, Tag, Product


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
        fields = ["review", "rating",]
        

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