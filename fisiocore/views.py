from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Patient, Anamnesis
from .forms import PatientForm, AnamnesisForm

MAIN_MENU_ITEMS = [
    (_("Patients"), "fisiocore:patients", "fa-home"),
    (_("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (_("Informed consent"), "fisiocore:consents", "fa-pen-alt"),
    (_("Invoicing"), "fisiocore:invoices", "fa-credit-card"),
]


@login_required
def patients(request):
    patients = Patient.objects.filter(user=request.user)
    context = {
        'title': _("Patients"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patients': patients
    }
    return render(request, 'fisiocore/patients.html', context)


@login_required
def view_patient(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404(_("There is no patient with Id {0}").format(patient_id))
    if patient.user != request.user:
        raise Http403(_("You are not allowed to see the data of this user"))
    context = {
        'title': _('Patient "{0}"'.format(patient)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient
    }
    return render(request, 'fisiocore/patient.html', context)


@login_required
def add_patient(request):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add patient"
    }
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect(reverse('fisiocore:view_patient', args=[patient.id]))
        else:
            rendered_form = form.render('fisiocore/patient_form.html')
            context['form'] = rendered_form
            return render(request, 'fisiocore/add_patient.html', context)
    form = PatientForm(initial={'user':request.user.id})
    rendered_form = form.render('fisiocore/patient_form.html')
    context['form'] = rendered_form
    return render(request, 'fisiocore/add_patient.html', context)
    

@login_required
def edit_patient(request, patient_id):
    if request.method == "POST":
        patient = Patient.objects.get(pk=patient_id)
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:view_patient', args=[patient_id]))
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404(_("There is no patient with Id {0}").format(patient_id))
    if patient.user != request.user:
        raise Http403(_("You are not allowed to see the data of this user"))
    form = PatientForm(instance=patient)
    rendered_form = form.render('fisiocore/patient_form.html')
    context = {
        'title': _('Edit Patient "{0}"'.format(patient)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'form': rendered_form
    }
    return render(request, 'fisiocore/edit_patient.html', context)
    

@login_required
def delete_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    if request.method == "POST":
        if request.POST.get('confirm') is not None:
            patient.delete()
            return redirect(reverse('fisiocore:patients'))
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'title': _('Delete patient {0} {1}'.format(patient.first_name, patient.last_name)),
        'patient': patient
    }
    return render(request, 'fisiocore/delete_patient.html', context)
    
    
@login_required
def anamnesis(request, patient_id, anamnesis_id=None):
    patient = Patient.objects.get(pk=patient_id)
    try:
        anamnesis = Anamnesis.objects.get(pk=anamnesis_id)
    except Anamnesis.DoesNotExist:
        anamnesis = None
    anamnesis_list = Anamnesis.objects.filter(patient=patient_id)
    context = {
        'title': _('Clinical history "{0}"'.format(patient)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'anamnesis_list': anamnesis_list,
        'anamnesis': anamnesis,
    }
    return render(request, 'fisiocore/anamnesis.html', context)
    
def add_anamnesis(request, patient_id):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add Anamnesis"
    }
    if request.method == "POST":
        form = AnamnesisForm(request.POST)
        if form.is_valid():
            anamnesis = form.save()
            return redirect(reverse('fisiocore:anamnesis', args=[patient_id, anamnesis.id]))
        else:
            rendered_form = form.render('fisiocore/anamnesis_form.html')
            context['form'] = rendered_form
            context['patient_id'] = patient_id
            return render(request, 'fisiocore/add_anamnesis.html', context)
    form = AnamnesisForm(initial={'user': request.user.id, 'patient': patient_id})
    rendered_form = form.render('fisiocore/anamnesis_form.html')
    context['form'] = rendered_form
    context['patient_id'] = patient_id
    return render(request, 'fisiocore/add_anamnesis.html', context)
    
def edit_anamnesis(request, anamnesis_id):
    if request.method == "POST":
        anamnesis = Anamnesis.objects.get(pk=anamnesis_id)
        form = AnamnesisForm(request.POST, instance=anamnesis)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:anamnesis', args=[anamnesis.patient.id, anamnesis_id]))
        # return redirect(reverse('fisiocore:anamnesis', args=[anamnesis.patient]))
    try:
        anamnesis = Anamnesis.objects.get(pk=anamnesis_id)
    except Anamnesis.DoesNotExist:
        raise Http404(_("There is no Anamnesis with Id {0}").format(anamnesis_id))
    if anamnesis.user != request.user:
        raise Http403(_("You are not allowed to see the data of this user"))
    form = AnamnesisForm(instance=anamnesis)
    rendered_form = form.render('fisiocore/anamnesis_form.html')
    context = {
        'title': _('Edit Anamnesis "{0}"'.format(anamnesis)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'anamnesis': anamnesis,
        'form': rendered_form
    }
    return render(request, 'fisiocore/edit_anamnesis.html', context)
    
def delete_anamnesis(request, anamnesis_id):
    pass
    
def add_consent(request):
    pass

def revoke_consent(request, consent_id):
    pass


def consents(request):
    pass
    
def calendar(request):
    pass
    
def invoices(request):
    pass
