from django.forms import Form, ModelForm, CharField, FileField, DurationField
from django.forms.widgets import DateInput, TimeInput, NumberInput
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import ListPrice

class ListPriceForm(ModelForm):
    class Meta:
        model = ListPrice
        fields = [
            'user',
            'description', 
            'conditions', 
            'duration', 
            'netprice', 
            'vat'
        ]
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'input'})
        self.fields['conditions'].widget.attrs.update({'class': 'input'})
        self.fields['vat'].widget.attrs.update({'class': 'input'})
        self.fields['duration'].widget.attrs.update({'class': 'input'})
        self.fields['netprice'].widget.attrs.update({'class': 'input', 'min':'1', 'max':'1000', 'step':".01", 'placeholder':"0.00", })
