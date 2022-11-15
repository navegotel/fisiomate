from django.urls import path, re_path
from django.contrib.auth.views import LoginView, logout_then_login
from . import views

app_name = 'fisiocore'

urlpatterns = [
    path('', views.patients, name='patients'),
    path('patient/add', views.add_patient, name='add_patient'),
    path('patient/view/<int:patient_id>', views.view_patient, name='view_patient'),
    path('patient/edit/<int:patient_id>', views.edit_patient, name='edit_patient'),
    path('patient/delete/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('patient/addconsent/<int:patient_id>', views.add_consent, name='add_consent'),
    path('patient/revokeconsent/<int:consent_id>', views.revoke_consent, name='revoke_consent'),
    path('patient/examination/<int:patient_id>', views.examination, name='examination'),
    path('patient/examination/<int:patient_id>/<int:examination_id>', views.examination, name='examination'),
    path('patient/addanamnesis/<int:patient_id>', views.add_examination, name='add_examination'),
    path('patient/editanamnesis/<int:examination_id>', views.edit_examination, name='edit_examination'),
    path('patient/deleteanamnesis/<int:examination_id>', views.delete_examination, name='delete_examination'),
    path('patient/addimages/<int:examination_id>', views.add_images, name='add_images'),
    path('consents', views.consents, name='consents'),
    path('calendar', views.calendar, name='calendar'),
    path('invoices', views.invoices, name='invoices'),
    path('login', LoginView.as_view(template_name = "fisiocore/login.html"), name='login'),
    path('logout', logout_then_login, name='logout'),
    re_path('^media/medical_images/\w+', views.medical_image, name='medical_image')
]
