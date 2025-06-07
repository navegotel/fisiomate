from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from fisiocore.models import Patient


class ListPrice(models.Model):
    
    class Meta:
        ordering = ['description',]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(_("Creation date"), auto_now_add=True)
    last_update = models.DateField(_("Last update"), auto_now=True)
    description = models.CharField(_("Description"), max_length=200)
    conditions = models.CharField(_("Conditions"), max_length=200, blank=True)
    duration = models.DurationField(_("Duration"))
    netprice = models.DecimalField(_("Net Price"), max_digits=6, decimal_places=2)
    vat = models.DecimalField(_("Value Added Tax"), max_digits=2, decimal_places=0)
    price = models.GeneratedField(
        db_persist = False,
        output_field = models.DecimalField(max_digits=6, decimal_places=2),
        expression = models.F("netprice") + (models.F("netprice") * (models.F('vat') / 100.0))
    )
    
    def __str__(self):
        return "{0} - {1}".format(self.description, self.price)


class Quote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return _("Quote nbr {0} for patient {1}").format(self.id, self.patient)
    
    
class QuoteItem(models.Model):
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE, related_name='items')
    quantity = models.SmallIntegerField(_("Quantity"))
    description = models.CharField(_("Description"), max_length=200)
    netprice = models.DecimalField(_("Price"), max_digits=6, decimal_places=2)
    vat = models.PositiveSmallIntegerField(_("Value Added Tax"))
    price = models.GeneratedField(
        db_persist = False,
        output_field = models.DecimalField(max_digits=6, decimal_places=2),
        expression = models.F("netprice") + (models.F("netprice") * (models.F('vat') / 100.0))
    )
    
    
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


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(_("Quantity"))
    description = models.CharField(_("Description"), max_length=200)
    netprice = models.DecimalField(_("Price"), max_digits=6, decimal_places=2)
    vat = models.PositiveSmallIntegerField(_("Value Added Tax"))
    price = models.GeneratedField(
        db_persist = False,
        output_field = models.DecimalField(max_digits=6, decimal_places=2),
        expression = models.F("netprice") + (models.F("netprice") * (models.F('vat') / 100.0))
    )
    

class Receipt(models.Model):
    """Payment receipt."""
    first_name = models.CharField(_("First name"), max_length=50)
    second_name = models.CharField(_("Last name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    post_code = models.CharField(_("Post code"), max_length=10)
    street = models.CharField(_("Street"), max_length=10)
    date = models.DateField()
    

class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
