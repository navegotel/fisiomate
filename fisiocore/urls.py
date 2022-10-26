from django.urls import path
from . import views

app_name = 'fisiocore'

urlpatterns = [
    path('', views.patients, name='patients'),
    path('patient/add', views.add_patient, name='patient'),
    path('patient/view/<int:patient_id>', views.patient, name='view_patient'),
    path('patient/edit/<int:patient_id>', views.edit_patient, name='edit_patient'),
    path('patient/delete/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('patient/addconsent/<int:patient_id>', views.add_consent, name='add_consent'),
    path('patient/addanamnesis/<int:patient_id>', views.add_anamnesis, name='add_anamnesis'),
    path('login', views.login, name='login'),
]
