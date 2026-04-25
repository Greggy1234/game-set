from django import forms
from .models import ShopOrder, BookingOrder


class ShopOrderForm(forms.ModelForm):
    class Meta:
        model = ShopOrder
        fields = ('full_name', 'email', 'phone_number', 'street_address1', 
                  'street_address2', 'town_or_city', 'postcode', 'country', 'county',)
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders to SHOP hub checkout form
        """        
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }
        
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].label = False



class BookingOrderForm(forms.ModelForm):
    class Meta:
        model = ShopOrder
        fields = ('full_name', 'email', 'phone_number', 'street_address1', 
                  'street_address2', 'town_or_city', 'postcode', 'country', 'county',)
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders to BOOK hub checkout form
        """        
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'GB',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }
        
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            else:
                self.fields[field].disabled = True
                self.fields[field].initial = "GB"
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].label = False