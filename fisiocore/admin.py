from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, UserProfile, TreatmentPlan, Session, Invoice, Payment, Receipt, Examination, MedicalImage, ClinicalDocument, InformedConsentDocument

class PatientAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "user profiles"
    
    
class TreatmentPlanAdmin(admin.ModelAdmin):
    pass
    
    
class SessionAdmin(admin.ModelAdmin):
    pass
    
    
class InvoiceAdmin(admin.ModelAdmin):
    pass
    

class PaymentAdmin(admin.ModelAdmin):
    pass
    
    
class ReceiptAdmin(admin.ModelAdmin):
    pass
    
    
class MedicalImageInline(admin.StackedInline):
    model = MedicalImage
    can_delete = True

class ClinicalDocumentInline(admin.StackedInline):
    model = ClinicalDocument
    can_delete = True
    
    
class AnamnesisAdmin(admin.ModelAdmin):
    inlines = (MedicalImageInline, ClinicalDocumentInline)
    
    
    
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


class InformedConsentDocumentAdmin(admin.ModelAdmin):
    model = InformedConsentDocument


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(TreatmentPlan, TreatmentPlanAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Examination, AnamnesisAdmin)
admin.site.register(InformedConsentDocument, InformedConsentDocumentAdmin)
