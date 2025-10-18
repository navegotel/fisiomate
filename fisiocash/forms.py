from django.forms import Form, ModelForm, CharField, FileField, DurationField
from django.forms.widgets import DateInput, TimeInput, NumberInput
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.forms.widgets import DateInput
from .models import ListPrice, Quote, QuoteItem

class ListPriceForm(ModelForm):
    template_name = 'fisiocash/price_form.html'
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

class QuoteForm(ModelForm):
    template_name = 'fisiocash/quote_form.html'
    class Meta:
        model = Quote
        fields = [
            'user',
            'patient',
            'date',
            'status',
        ]
        
        widgets = {
            'date': DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'class': 'input'}),
        }
        
class QuoteItemForm(ModelForm):
    class Meta:
        model = QuoteItem
        fields = [
            'quantity',
            'description',
            'net_unit_price',
            'vat',
        ]
