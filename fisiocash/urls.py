from django.urls import path, re_path
from . import views

app_name = 'fisiocash'

urlpatterns = [
    path('invoicing/receipts', views.invoices, name='receipts'),
    path('invoicing/invoices', views.invoices, name='invoices'),
    path('invoicing/pricingtable', views.invoices, name='pricing_table'),
    path('templates/invoice', views.show_invoice_template),
]


