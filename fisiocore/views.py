from django.shortcuts import render
from django.utils.translation import gettext as _
from .models import Patient

MAIN_MENU_ITEMS = [
    (_("Patients"), "fisiocore:patients", "fa-home"),
    (_("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (_("Informed consent"), "fisiocore:consents", "fa-pen-alt"),
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
    

def patient(request):
    pass
    

def add_patient(request):
    pass
    

def edit_patient(request):
    pass
    
    
def delete_patient(request):
    pass
    
    
def add_consent(request):
    pass


def add_anamnesis(request):
    pass

def consents(request):
    pass
    
def calendar(request):
    pass
