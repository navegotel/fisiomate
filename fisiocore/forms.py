from django.forms import Form, ModelForm, CharField, FileField
from django.forms.widgets import DateInput, TimeInput, NumberInput
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import Patient, Examination, MedicalImage, ClinicalDocument, Session, InformedConsentDocument, InformedConsent, ExplorationTemplate, TreatmentPlan


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
            'habits',
            'medical_conditions',
            'remarks'
        ]


class ExaminationForm(ModelForm):
    class Meta:
        model = Examination
        fields = [
            'user',
            'therapist',
            'patient',
            'reason',
            'interview',
            'exploration',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['therapist'].queryset = User.objects.filter(groups__name='Therapist')


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

class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = [
            'user',
            'therapist',
            'patient',
            'date',
            'start',
            'end',
            'treatment_plan',
            'completed',
            'remarks',
        ]
        widgets = {
            'date': DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'class': 'input'}),
            'start': TimeInput(attrs={'type': 'time', 'class': 'input'}),
            'end': TimeInput(attrs={'type': 'time', 'class': 'input'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['therapist'].queryset = User.objects.filter(groups__name='Therapist')
        self.fields['patient'].widget.attrs.update({'class':'select'})
        self.fields['therapist'].widget.attrs.update({'class':'select'})
        self.fields['treatment_plan'].widget.attrs.update({'class':'select'})
        self.fields['completed'].widget.attrs.update({'class':'select'})
        self.fields['remarks'].widget.attrs.update({'class':'textarea'})
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

class InformedConsentDocumentForm(ModelForm):
    class Meta:
        model = InformedConsentDocument
        fields = [
            'user',
            'title',
            'language',
            'body',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'select'})
        

class InformedConsentForm(ModelForm):
    class Meta:
        model = InformedConsent
        fields = [
            'user',
            'patient',
            'consent_type',
            'revoked',
            'signed_consent'
        ]
        
        widgets = {
            'revoked': DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'class': 'input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['signed_consent'].widget.attrs.update({'class': 'input'})
        self.fields['consent_type'].widget.attrs.update({'disabled': 'true'})


class ExplorationTemplateForm(ModelForm):
    class Meta:
        model = ExplorationTemplate
        fields = [
            'user',
            'title',
            'anamnesis',
            'exploration'
        ]
        
class TreatmentPlanForm(ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = [
        'user',
            'patient',
            'name',
            'description',
            'number_of_sessions',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number_of_sessions'].widget.attrs.update({'class': 'input', 'min':'1', 'max':'20'})
