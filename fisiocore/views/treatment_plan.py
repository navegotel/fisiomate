
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, TreatmentPlan
from ..menu import MAIN_MENU_ITEMS

  
@login_required
def view_treatmentplans(request, patient_id, treatmentplan_id=None):
    patient = Patient.objects.get(pk=patient_id)
    context= {
        'title': _("Treatment plans for {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'buttonlabel': 'Add Treatment plan',
    }
    if treatmentplan_id is None:
        queryset = TreatmentPlan.objects.filter(patient=patient_id)
        print(queryset)
        if queryset:
            return redirect(reverse('fisiocore:view_treatmentplans', args=[patient_id, queryset.latest('creation_date').id]))
        else:
            return render(request, 'fisiocore/treatment_plan/view_treatmentplans.html', context)
    treatmentplans = TreatmentPlan.objects.filter(patient=patient.id)
    treatmentplan = TreatmentPlan.objects.get(pk=treatmentplan_id)
    context['treatmentplan'] = treatmentplan
    context['treatmentplans'] = treatmentplans
    return render(request, 'fisiocore/treatment_plan/view_treatmentplans.html', context)


@login_required
def add_treatmentplan(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    context= {
        'title': _("New treatment plan for {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
    }
    return render(request, 'fisiocore/add.html', context)
