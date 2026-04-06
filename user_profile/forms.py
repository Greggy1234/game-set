from django import forms
from .models import Profile


class ProfileInfo(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'years_playing', 'fave_surface', 'fave_shot',)
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto-generated labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False


class ProfileStatsYear(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('years_playing',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['years_playing'].label = "Year's you've been playing"
        
        
class ProfileStatsSurface(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fave_surface',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fave_surface'].label = "Your Favourite Surface"
        
        
class ProfileStatsShot(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fave_shot',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fave_shot'].label = "Your Favourite Shot"