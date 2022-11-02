from django.urls import path
from . import views

app_name = 'fisiocore'

urlpatterns = [
    path('', views.patients, name='patients'),
    path('patient/add', views.add_patient, name='add_patient'),
    path('patient/view/<int:patient_id>', views.view_patient, name='view_patient'),
    path('patient/edit/<int:patient_id>', views.edit_patient, name='edit_patient'),
    path('patient/delete/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('patient/addconsent/<int:patient_id>', views.add_consent, name='add_consent'),
    path('patient/revokeconsent<int:consent_id>', views.revoke_consent, name='revoke_consent'),
    path('patient/addanamnesis/<int:patient_id>', views.add_anamnesis, name='add_anamnesis'),
    path('consents', views.consents, name='consents'),
    path('calendar', views.calendar, name='calendar'),
    path('invoices', views.invoices, name='invoices'),
    path('login', views.UserLogin.as_view(), name='login'),
]
