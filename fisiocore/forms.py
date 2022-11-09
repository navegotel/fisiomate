from django.forms import Form, ModelForm, CharField
from .models import Patient, Examination, MedicalImage

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

class ExaminationForm(ModelForm):
    class Meta:
        model = Examination
        fields = [
            'user',
            'patient',
            'reason',
            'interview',
            'exploration',
        ]

class MedicalImageForm(ModelForm):
    class Meta:
        model = MedicalImage
        fields = [
            'patient',
            'examination',
            'image_type',
            'description',
            'image',
        ]
