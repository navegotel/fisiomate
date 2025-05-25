from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from ..models import Patient
from ..forms import PatientForm
from ..menu import MAIN_MENU_ITEMS

@login_required
def patients(request):
    patients = Patient.objects.filter(user=request.user)
    context = {
        'title': _("Patients"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patients': patients
    }
    return render(request, 'fisiocore/patient/patients.html', context)


# @login_required
def view_patient(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404(_("There is no patient with Id {0}").format(patient_id))
    context = {
        'title': _('Patient'),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient
    }
    return render(request, 'fisiocore/patient/patient.html', context)


@login_required
def add_patient(request):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add patient",
        'buttonlabel': _('Add patient')
    }
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect(reverse('fisiocore:view_patient', args=[patient.id]))
        else:
            rendered_form = form.render('fisiocore/patient/patient_form.html')
            context['form'] = rendered_form
            return render(request, 'fisiocore/add.html', context)
    form = PatientForm(initial={'user':request.user.id})
    rendered_form = form.render('fisiocore/patient/patient_form.html')
    context['form'] = rendered_form
    return render(request, 'fisiocore/add.html', context)
    

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
    rendered_form = form.render('fisiocore/patient/patient_form.html')
    context = {
        'title': _('Edit Patient'),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'form': rendered_form,
        'buttonlabel': _('Save changes')
    }
    return render(request, 'fisiocore/add.html', context)
    

@login_required
def delete_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    if request.method == "POST":
        if request.POST.get('confirm') is not None:
            patient.delete()
            return redirect(reverse('fisiocore:patients'))
    context = {
        'title': _('Delete patient'),
        'patient': patient
    }
    return render(request, 'fisiocore/patient/delete_patient.html', context)
