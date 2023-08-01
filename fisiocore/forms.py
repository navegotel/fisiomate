from django.forms import Form, ModelForm, CharField, FileField
from django.forms.widgets import DateInput, TimeInput, NumberInput
from django.utils.translation import gettext as _
from .models import Patient, Examination, MedicalImage, ClinicalDocument, Session


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


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = [
            'user',
            'patient',
            'date',
            'start',
            'end',
            'session_number',
            'treatment_plan',
            'completed',
            'remarks',
            'price',
        ]
        widgets = {
            'date': DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'class': 'input'}),
            # 'start': TimeInput(attrs={'tupe': 'time', 'class': 'input'}),
            # 'end': TimeInput(attrs={'tupe': 'time', 'class': 'input'}),
            'session_number': NumberInput(attrs={'type': 'number', 'class': 'input'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({'class':'select'})
        self.fields['treatment_plan'].widget.attrs.update({'class':'select'})
        self.fields['remarks'].widget.attrs.update({'class':'textarea'})
        self.fields['price'].widget.attrs.update({'class':'input'})
        self.fields['start'].widget.attrs.update({'class': 'input'})
        self.fields['end'].widget.attrs.update({'class': 'input'})


class ClinicalDocumentForm(ModelForm):
    class Meta:
        model = ClinicalDocument
        fields = [
            'patient',
            'examination',
            'label',
            'upload',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].widget.attrs.update({'class': 'input'})
