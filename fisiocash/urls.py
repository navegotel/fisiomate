from django.urls import path, re_path
from . import views

app_name = 'fisiocash'

urlpatterns = [
    path('invoicing', views.dashboard, name='dashboard'),
    path('invoicing/quotes', views.quotes, name='quotes'),
    path('invoicing/quotes/<int:year>/<int:month>', views.quotes_by_month, name='quotes_by_month'),
    path('invoicing/quotes/patient', views.quotes_by_patient, name='quotes_by_patient'),
    path('invoicing/quotes/<int:patient_id>', views.quotes_by_patient, name='quotes_by_patient'),
    path('invoicing/invoices', views.invoices, name='invoices'),
    path('invoicing/invoices/<int:year>/<int:month>', views.invoices_by_month, name='invoices_by_month'),
    path('invoicing/invoices/patient', views.invoices_by_patient, name='invoices_by_patient'),
    path('invoicing/invoices/<int:patient_id>', views.invoices_by_patient, name='invoices_by_patient'),
    path('invoicing/pricelist', views.pricelist, name='pricelist'),
    path('invoicing/pricelist/add', views.add_price, name='add_price'),
    path('invoicing/pricelist/edit/<int:price_id>', views.edit_price, name='edit_price'),
    path('invoicing/pricelist/view/<int:price_id>', views.view_price, name='view_price'),
]


