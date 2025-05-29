from django.contrib import admin
from .models import HelpDoc

class HelpDocAdmin(admin.ModelAdmin):
    pass
    

admin.site.register(HelpDoc, HelpDocAdmin)
