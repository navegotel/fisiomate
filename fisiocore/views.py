from django.shortcuts import render
from django.http import Http404
from django.utils.translation import gettext as _
from .models import Patient

MAIN_MENU_ITEMS = [
    (_("Patients"), "fisiocore:patients", "fa-home"),
    (_("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (_("Informed consent"), "fisiocore:consents", "fa-pen-alt"),
    (_("Invoicing"), "fisiocore:invoices", "fa-credit-card"),
]


def login(request):
    context = {}
    return render(request, 'fisiocore/login.html', context)


def patients(request):
    patients = Patient.objects.all()
    context = {
        'title': _("Patients"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patients': patients
    }
    return render(request, 'fisiocore/patients.html', context)
    

def view_patient(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404(_("There is no patient with Id {0}").format(patient_id))
    context = {
        'title': _("Patient"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient
    }
    return render(request, 'fisiocore/patient.html', context)

def add_patient(request):
    pass
    

def edit_patient(request, patient_id):
    pass
    
    
def delete_patient(request, patient_id):
    pass
    
    
def add_consent(request):
    pass


def add_anamnesis(request):
    pass

def consents(request):
    pass
    
def calendar(request):
    pass
    
def invoices(request):
    pass
