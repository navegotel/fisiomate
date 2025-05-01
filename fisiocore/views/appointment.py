import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Session, TreatmentPlan
from ..forms import SessionForm
from ..menu import MAIN_MENU_ITEMS


@login_required
def view_sessions(request, patient_id, session_id=None):
    patient = Patient.objects.get(pk=patient_id)
    sessions = Session.objects.filter(patient=patient.id).order_by('-date')
    if session_id is None:
        if len(sessions) > 0:
            return redirect(reverse('fisiocore:view_sessions', args=[patient_id, sessions[0].id]))
        else:
            session = None
    else:
        session = Session.objects.get(pk=session_id)
    context = {
        'title': _('Treatment Sessions for {0}'.format(patient)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'sessions':sessions,
        'session': session,
    }
    return render(request, 'fisiocore/appointment/view_appointments.html', context)


@login_required
def add_session(request):
    patient_id = request.GET.get('patient')
    treatmentplan_id = request.GET.get('treatmentplan')
    context = {
        'title': "Add appointment",
        'buttonlabel': "Add appointment",
        'cancelurl': reverse('fisiocore:calendar'),
        'main_menu_items': MAIN_MENU_ITEMS,
    }
    if request.method == "GET":
        initial_data = {
            'date': request.GET.get('date'),
            'patient': patient_id,
            'treatment_plan': treatmentplan_id,
            'user': request.user.id,
        }
        if patient_id is not None:
            patient = Patient.objects.get(pk=patient_id)
            patient.in_treatment = True
            patient.save()
        form = SessionForm(initial=initial_data)
        if patient_id is not None:
            form.fields['treatment_plan'].queryset = TreatmentPlan.objects.filter(patient = patient_id)
        rendered_form = form.render('fisiocore/appointment/appointment_form.html') 
        context['form'] = rendered_form
        context['date'] = datetime.date.fromisoformat(request.GET.get('date'))
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:calendar_day', args=[form.cleaned_data['date'].year, form.cleaned_data['date'].month, form.cleaned_data['date'].day]))
        else:
            rendered_form = form.render('fisiocore/appointment/appointment_form.html') 
            context['form'] = rendered_form
            context['date'] = form.cleaned_data['date']
    return render(request, 'fisiocore/add.html', context)


@login_required
def edit_session(request, session_id):
    session = Session.objects.get(pk=session_id)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:calendar_day', args=[form.cleaned_data['date'].year, form.cleaned_data['date'].month, form.cleaned_data['date'].day]))
    form = SessionForm(instance=session)
    form.fields['treatment_plan'].queryset = TreatmentPlan.objects.filter(patient = form['patient'].value())
    rendered_form = form.render('fisiocore/appointment/appointment_form.html') 
    context = {
        'title': 'Edit appointment',
        'main_menu_items': MAIN_MENU_ITEMS,
        'date': session.date,
        'form': rendered_form,
    }
    return render(request, 'fisiocore/appointment/edit_appointment.html', context)


@login_required
def delete_session(request, session_id):
    session = Session.objects.get(pk=session_id)
    if request.method == "POST":
        if request.POST.get('confirm') is not None:
            session.delete()
            return redirect(reverse('fisiocore:calendar_day', args=[session.date.year, session.date.month, session.date.day]))
    context = {
        'title': 'Delete appointment',
        'main_menu_items': MAIN_MENU_ITEMS,
        'session': session,
    }
    return render(request, 'fisiocore/appointment/delete_appointment.html', context)
	

@login_required
def session_list(request, patient_id, session_id=None):
    if session_id is None:
        pass
