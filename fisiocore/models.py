import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _  


class UserProfile(models.Model):
    """Every user has his own patients, treatment plans, sessions and invoicing"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_("The login user"))
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    city = models.CharField(_("City"), max_length=50)
    province = models.CharField(_("Province"), max_length=50, blank=True, null=True)
    post_code = models.CharField(_("Postal code"), max_length=10, blank=True, null=True)
    street = models.CharField(_("Street"), max_length=50)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    

class Patient(models.Model):
    
    class Meta:
        ordering = ['last_name', 'first_name', 'date_of_birth', 'post_code']
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    date_of_birth = models.DateField(_("Date of birth"))
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=100)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    id_card_number = models.CharField(_("Id card"), max_length=20, blank=True, null=True)
    in_treatment = models.BooleanField(_("In treatment"))
    habits = models.TextField(_("Habits"), blank="True", null="True")
    medical_conditions = models.TextField(_("Medical conditions"), blank="True", null="True")
    remarks = models.TextField(_("Remarks"), blank="True", null="True")
    
    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)
    
    
class Examination(models.Model):

    class Meta:
        ordering = ['-last_update', '-creation_date']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="examination_therapist")
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    reason = models.CharField(_('Reason'), max_length=50)
    interview = models.TextField(_("Anamnesis"), help_text=_("Any health related information given by the patient."))
    exploration = models.TextField(_("Exploration"))
    
    def __str__(self):
        return "{0} {1}: {2}".format(self.patient.first_name, self.patient.last_name, self.reason)
    

def clinical_document_upload_name(instance, filename):
    ext = filename.split('.')[-1]
    return "clinical_documents/{0}/{1}/{2}.{3}".format(instance.patient.id, instance.examination.id, uuid4().hex, ext)


class ClinicalDocument(models.Model):
    
    class Meta:
        ordering = ['-last_update', '-creation_date']

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    examination = models.ForeignKey('Examination', on_delete= models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    label = models.CharField(_('Description'), max_length=200, help_text=_('A brief description of the attached document'))
    upload = models.FileField(_('URL'), upload_to=clinical_document_upload_name)
    

def medical_image_upload_name(instance, filename):
    ext = filename.split('.')[-1]
    return "medical_images/{0}/{1}/{2}.{3}".format(instance.patient.id, instance.examination.id, uuid4().hex, ext)

    
class MedicalImage(models.Model):

    class Meta:
        ordering = ['-last_update', '-creation_date']

    IMAGE_TYPE_CHOICES=[
        ('FOTO', _('Photography')),
        ('SKTC', _('Sketch')),
        ('XRAY', _('X-Ray')),
        ('ECHO', _('Ultrasound')),
        ('TAC', _('CT scan')),
        ('RMN', _('Nuclear magnetic resonance')),
        ('UNKN', _('Unknown/other'))
    ]
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    examination = models.ForeignKey('Examination', on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    image_type = models.CharField(_("Image type"), max_length=4, choices=IMAGE_TYPE_CHOICES, default='UNKN')
    projection = models.CharField(_("Projection"), max_length=20, blank=True, null=True)
    description = models.CharField(_('Image description'), max_length=200, blank=True, null=True, help_text=_("Findings or explanation of what is depicted in the image"))
    image = models.ImageField(upload_to=medical_image_upload_name)
    
    
class PatientReport(models.Model):
    """Report for handing out to patient."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    report = models.TextField(_("Patient report"))
    

class TreatmentPlanTemplate(models.Model):
    """Generic treatment plans from which individual treatment plans can be tailored"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50, help_text=_("Descriptive name for the treatment plan."))
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text=_("Overall price of the whole treatment plan."))
    session_count = models.PositiveSmallIntegerField(default=1)


class TreatmentPlan(models.Model):
    """Individual treatment plan for a specific patient"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    examination = models.ForeignKey('Examination', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=50, help_text=_("Descriptive name for the treatment plan."))
    description = models.TextField(help_text=_("Detailed description of the treatment plan. Supports Markdown"))
    number_of_sessions = models.SmallIntegerField(_("Number of sessions"))
 

    def __str__(self):
        return self.name
    
    
class Session(models.Model):
    class Meta:
        ordering = ['-date', 'start']
        
    COMPLETED_CHOICES=[
        (0, _('Booked')),
        (1, _('Completed')),
        (2, _('Cancelled')),
        (3, _('No Show')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="session_therapist")
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, limit_choices_to={"in_treatment": True})
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    treatment_plan = models.ForeignKey('TreatmentPlan', on_delete=models.CASCADE, blank=True, null=True)
    completed = models.IntegerField(_("Completed"), choices=COMPLETED_CHOICES, default=0)
    remarks = models.TextField(help_text=_("Anything remarkable such as patient's progress"), blank=True, null=True)
    
    def __str__(self):
        return "{0}, {1} - {2}: {3}".format(self.date, self.start, self.end, self.patient)
        
    class Meta:
        ordering = ["date", "start"]


class InformedConsentDocument(models.Model):
    """Document that needs to be signed by patient and uploaded"""
    LANGUAGE_CHOICES=[
        ('EN', _('English')),
        ('ES', _('Spanish')),
        ('FR', _('French')),
        ('DE', _('German')),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    title = models.CharField(_("Title"), max_length=50)
    language = models.CharField(_("Language"), max_length=2, choices=LANGUAGE_CHOICES, default='EN')
    body = models.TextField(_("Body"))

    def __str__(self):
        return self.title
    
def informed_consent_upload_name(instance, filename):
    ext = filename.split('.')[-1]
    return "igned_consent/{0}/{1}.{2}".format(instance.patient.id, instance.consent_type.id, ext)

class InformedConsent(models.Model):
    """Upload of signed pdf. This can be a paper scan or an 
    electronically signed pdf"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    consent_type = models.ForeignKey('InformedConsentDocument', on_delete=models.CASCADE)
    signed_consent = models.FileField(_("Informed consent"), upload_to=informed_consent_upload_name)
    
    def __str__(self):
        return "{0}, {1}".format(self.patient, self.consent_type.title)
    

class ExplorationTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    title = models.CharField(_("Title"), max_length=50)
    anamnesis = models.TextField(_("Anamnesis"), blank=True, null=True)
    exploration = models.TextField(_("Exploration"), blank=True, null=True)


    def __str__(self):
        return self.title




