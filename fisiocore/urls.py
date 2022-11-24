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
    path('patient/listimages/<int:patient_id>', views.imagelist, name='imagelist'),
    path('patient/listimages/<int:patient_id>/<int:image_id>', views.imagelist, name='imagelist'),
    path('patient/addanamnesis/<int:patient_id>', views.add_examination, name='add_examination'),
    path('patient/editanamnesis/<int:examination_id>', views.edit_examination, name='edit_examination'),
    path('patient/deleteanamnesis/<int:examination_id>', views.delete_examination, name='delete_examination'),
    path('patient/addimages/<int:examination_id>', views.add_images, name='add_images'),
    path('patient/viewimage/<int:image_id>', views.view_medical_image, name='view_medical_image'),
    path('patient/editimage/<int:image_id>', views.edit_medical_image, name='edit_medical_image'),
    path('patient/deleteimage/<int:image_id>', views.delete_medical_image, name='delete_medical_image'),
    path('patient/adddocument/<int:examination_id>', views.add_document, name='add_document'),
    path('patient/viewdocument/<int:document_id>', views.view_document, name='view_document'),
    path('patient/editdocument/<int:document_id>', views.edit_document, name='edit_document'),
    path('patient/deletedocument/<int:document_id>', views.delete_document, name='delete_document'),
    path('consents', views.consents, name='consents'),
    path('calendar', views.calendar, name='calendar'),
    path('invoices', views.invoices, name='invoices'),
    path('login', LoginView.as_view(template_name = "fisiocore/login.html"), name='login'),
    path('logout', logout_then_login, name='logout'),
    re_path('^media/medical_images/\w+', views.medical_image, name='medical_image'),
    re_path('^media/clinical_documents/\w+', views.document, name='clinical_document')
]
