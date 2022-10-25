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
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    tax_number = models.CharField(_("Tax number"), max_length=50, blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to="logos/", blank=True, null=True)
    

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    first_name = models.CharField(_("First name"), max_length=50)
    second_name = models.CharField(_("Last name"), max_length=50)
    date_of_birth = models.DateField(_("Date of birth"))
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20)
    id_card_number = models.CharField(_("Id card"), max_length=20)
    ss_number = models.CharField(_("Social security number"), max_length=20)
    ss_country = models.CharField(_("Social security country"), max_length=2)
    ss_issue_date = models.DateField(_("Social security date of issue"))
    ss_expiry_date = models.DateField(_("Social security expiry date"))
    
class Anamnesis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    anamnesis = models.TextField(_("Anamnesis"), help_text=_("Any health related information given by the patient."))
    

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
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text=_("Overal price of the whole treatment plan."))    
    session_count = models.PositiveSmallIntegerField(default=1)


class TreatmentPlan(models.Model):
    """Individual treatment plan for a specific patient"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
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
    treatment_plan = models.ForeignKey('TreatmentPlan', on_delete=models.CASCADE)
    completed = models.BooleanField()
    remarks = models.TextField(help_text=_("Anything remarkable such as patient's progress"))
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE)
    
    
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
    first_name = models.CharField(_("First name"), max_length=50)
    second_name = models.CharField(_("Last name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=10)
    date = models.DateField()
    


class InformedConsentDocument(models.Model):
    pass
    
    
class InformedConsent(models.Model):
    pass
