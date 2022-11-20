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
            'projection',
            'description',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'input'})
        self.fields['projection'].widget.attrs.update({'class': 'input'})
        self.fields['image_type'].widget.attrs.update({'class': 'select'})
