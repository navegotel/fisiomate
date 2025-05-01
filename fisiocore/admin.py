from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, UserProfile, TreatmentPlan, Session, Examination, MedicalImage, ClinicalDocument, InformedConsentDocument, ExplorationTemplate

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
    pass


class ExplorationTemplateAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(TreatmentPlan, TreatmentPlanAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Examination, AnamnesisAdmin)
admin.site.register(InformedConsentDocument, InformedConsentDocumentAdmin)
admin.site.register(ExplorationTemplate, ExplorationTemplateAdmin)
