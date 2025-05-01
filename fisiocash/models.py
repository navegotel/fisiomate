from django.db import models
from django.utils.translation import gettext as _
from fisiocore.models import Patient

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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
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
