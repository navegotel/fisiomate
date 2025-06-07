from django.contrib import admin
from .models import ListPrice, Quote, QuoteItem, Payment, Invoice, InvoiceItem, Receipt

class ListPriceAdmin(admin.ModelAdmin):
    pass


class QuoteItemInlineAdmin(admin.StackedInline):
    model = QuoteItem
    can_delete = False
    verbose_name_plural = "quote items"
    

class QuoteAdmin(admin.ModelAdmin):
    inlines = (QuoteItemInlineAdmin,)


admin.site.register(ListPrice, ListPriceAdmin)
admin.site.register(Quote, QuoteAdmin)

