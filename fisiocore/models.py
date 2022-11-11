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
    tax_number = models.CharField(_("Tax number"), max_length=50, blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to="logos/", blank=True, null=True)
    

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
    ss_number = models.CharField(_("Social security number"), max_length=20, blank=True, null=True)
    ss_country = models.CharField(_("Social security country"), max_length=2, blank=True, null=True)
    ss_issue_date = models.DateField(_("Social security date of issue"), blank=True, null=True)
    ss_expiry_date = models.DateField(_("Social security expiry date"), blank=True, null=True)
    in_treatment = models.BooleanField(_("In treatment"))
    remarks = models.TextField(_("Remarks"), blank="True", null="True")
    
    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)
    
    
class Examination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    reason = models.CharField(_('Reason'), max_length=50)
    interview = models.TextField(_("Anamnesis"), help_text=_("Any health related information given by the patient."))
    exploration = models.TextField(_("Exploration"))
    
    def __str__(self):
        return "{0} {1}: {2}".format(self.patient.first_name, self.patient.last_name, self.reason)
    
    
class ClinicalDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    examination = models.ForeignKey('Examination', on_delete= models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    label = models.CharField(_('Description'), max_length=200, help_text=_('A brief description of the attached document'))
    upload = models.FileField(_('URL'), upload_to='uploads/%Y/%m/%d/')
    


def medical_image_upload_name(instance, filename):
    ext = filename.split('.')[-1]
    return "medical_images/{0}/{1}/{2}.{3}".format(instance.patient.id, instance.examination.id, uuid4().hex, ext)

    
class MedicalImage(models.Model):
    IMAGE_TYPE_CHOICES=[
        ('FOTO', _('Photography')),
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
    description = models.CharField(max_length=200, blank=True, null=True)
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
    examination = models.ForeignKey('Examination', on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50, help_text=_("Descriptive name for the treatment plan."))
    description = models.TextField(help_text=_("Detailed description of the treatment plan. Supports Markdown"))
    number_of_sessions = models.SmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text=_("Overal price of the whole treatment plan."))
    invoice = models.OneToOneField("Invoice", on_delete=models.CASCADE)
    active = models.BooleanField(_("Active"))
    
    
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    session_number = models.PositiveSmallIntegerField(default=1)
    treatment_plan = models.ForeignKey('TreatmentPlan', on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField()
    remarks = models.TextField(help_text=_("Anything remarkable such as patient's progress"), blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return "{0}, {1} - {2}: {3}".format(self.date, self.start, self.end, self.patient)
        
    class Meta:
        ordering = ["date", "start"]
    
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    
    
class Invoice(models.Model):
    # Invoicing address may be different from patients address
    first_name = models.CharField(_("First name"), max_length=50)
    second_name = models.CharField(_("Last name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=10)
    date = models.DateField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if len(self.first_name) == 0:
            self.first_name = self.patient.first_name
        if len(self.second_name) == 0:
            self.second_name = self.patient.second_name
            
        super().save(*args, **kwargs)
    

class Receipt(models.Model):
    """Payment receipt."""
    first_name = models.CharField(_("First name"), max_length=50)
    second_name = models.CharField(_("Last name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=10)
    date = models.DateField()
    


class InformedConsentDocument(models.Model):
    """Document that needs to be signed by patient and uploaded"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    
    
    
class InformedConsent(models.Model):
    """Upload of signed pdf. This can be a paper scan or an 
    electronically signed pdf"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    signed_consent = models.FileField(_("Informed consent"), upload_to="signed_consent/")
    
