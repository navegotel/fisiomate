from django.forms import ModelForm
from .models import Patient

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = [
            'user',
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'city', 
            'post_code', 
            'street', 
            'email', 
            'phone', 
            'id_card_number',
            'ss_number',
            'ss_country',
            'ss_issue_date',
            'ss_expiry_date',
            'in_treatment',
            'remarks'
        ]
        

