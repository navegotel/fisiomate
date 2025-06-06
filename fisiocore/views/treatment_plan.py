from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, TreatmentPlan
from ..forms import TreatmentPlanForm
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
        if queryset:
            return redirect(reverse('fisiocore:view_treatmentplans', args=[patient_id, queryset.latest('creation_date').id]))
        else:
            return render(request, 'fisiocore/treatment_plan/view_treatmentplans.html', context)
    treatmentplans = TreatmentPlan.objects.filter(patient=patient.id)
    treatmentplan = TreatmentPlan.objects.get(pk=treatmentplan_id)
    context['treatmentplan'] = treatmentplan
    context['treatmentplans'] = treatmentplans
    return render(request, 'fisiocore/treatment_plan/view_treatmentplans.html', context)


#@login_required
def add_treatmentplan(request, patient_id):
    if request.method == 'POST':
        print(request.POST)
        form = TreatmentPlanForm(request.POST)
        if form.is_valid():
            treatment_plan = form.save()
            url = reverse('fisiocore:calendar')
            url += "?patient={0}&treatmentplan={1}".format(patient_id, treatment_plan.id)
            return redirect(url)
        else:
            print(form.errors)
    patient = Patient.objects.get(pk=patient_id)
    print(request.user.id)
    context= {
        'title': _("New treatment plan for {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
    }
    initial_data = {
        'patient': patient_id,
        'user': request.user.id,
    }
    form = TreatmentPlanForm(initial=initial_data)
    rendered_form = form.render('fisiocore/treatment_plan/treatmentplan_form.html') 
    context['form'] = rendered_form
    return render(request, 'add.html', context)
