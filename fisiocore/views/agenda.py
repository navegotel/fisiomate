import calendar
import datetime
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Session, TreatmentPlan
from ..menu import MAIN_MENU_ITEMS


MONTH_NAMES = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


@login_required    
def view_calendar(request, year=None, month=None):
    patient_id = request.GET.get('patient')
    treatmentplan_id = request.GET.get('treatmentplan')
    if year is None or month is None:
        url = reverse('fisiocore:calendar', args=[datetime.date.today().year, datetime.date.today().month])
        if patient_id is None:
            return redirect(url)
        else:
            url += "?patient="+patient_id
            if treatmentplan_id is not None:
                url += "&treatmentplan="+treatmentplan_id
            return redirect(url)
    if patient_id is not None:
        patient = Patient.objects.get(pk=patient_id)
    else:
        patient = None
    if treatmentplan_id is not None:
        treatmentplan = TreatmentPlan.objects.get(pk=treatmentplan_id)
    else:
        treatmentplan = None
    c = calendar.Calendar()
    current_day = 31
    today = datetime.date.today()
    if year == today.year: 
        if month == today.month:
            current_day = today.day
        elif month > today.month:
            current_day = 0
    elif year > today.year:
        current_day = 0
    if month > 1:
        prev_month = month - 1
        prev_year = year
    else:
        prev_month = 12
        prev_year = year - 1
    if month < 12:
        next_month = month + 1
        next_year = year
    else:
        next_month = 1
        next_year = year + 1
    if month < 11:
        nextnext_month = month + 2
        nextnext_year = year
    else:
        nextnext_month = month - 10
        nextnext_year = year + 1
    sessions = Session.objects.filter(user=request.user, date__year=year, date__month=month)
    title = _(MONTH_NAMES[month]) + ' ' + str(year)
    if patient is not None:
        title = "{0} (Patient: {1})".format(title, patient)
        
    context = {
        'title': title,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'nextnext_month': nextnext_month,
        'nextnext_year': nextnext_year,
        'month': month,
        'year': year,
        'month_name': _(MONTH_NAMES[month]),
        'prev_month_name': _(MONTH_NAMES[prev_month]),
        'next_month_name': _(MONTH_NAMES[next_month]),
        'nextnext_month_name': _(MONTH_NAMES[nextnext_month]),
        'main_menu_items': MAIN_MENU_ITEMS,
        'weeks': c.monthdays2calendar(year, month),
        'current_day': current_day,
        'today': today,
        'sessions': sessions,
        'patient': patient,
        'treatmentplan':treatmentplan
    }
    return render(request, 'fisiocore/calendar/calendar_month.html', context)


@login_required
def view_calendar_day(request, year, month, day):

    class FreeSlot(object):
        def __init__(self, start, end):
            self.free = True
            self.start = start
            self.end = end

        @property
        def duration(self):
            value = datetime.timedelta(hours=self.end.hour, minutes=self.end.minute) - datetime.timedelta(hours=self.start.hour, minutes=self.start.minute)
            return "{0:02d}:{1:02d}".format(int(value.seconds/3600), int((value.seconds%3600)/60))
        
        def __repr__(self):
            return "{0} - {1}".format(self.start, self.end)

    date = datetime.date(year, month, day)
    sessions = Session.objects.filter(user=request.user, date=date)
    slots = []
    for i in range(0, len(sessions)):
        slots.append(sessions[i])
        try:
            if sessions[i].end < sessions[i+1].start:
                slots.append(FreeSlot(sessions[i].end, sessions[i+1].start))
        except IndexError:
            pass

    title = date
    patient_id = request.GET.get("patient")
    if patient_id is None:
        patient = None
    else:
        patient = Patient.objects.get(pk=patient_id)
        #title = "{0}, (Patient: {1})".format(title, patient)
    treatmentplan_id = request.GET.get('treatmentplan')
    if treatmentplan_id is None:
        treatmentplan = None
    else:
        treatmentplan = TreatmentPlan.objects.get(pk=treatmentplan_id)

    context={
        'title': title,
        'main_menu_items': MAIN_MENU_ITEMS,
        'sessions': sessions,
        'slots': slots,
        'year':year,
        'month': month,
        'day': day,
        'date': date,
        'monthname': _(MONTH_NAMES[month]),
        'patient': patient,
        'treatmentplan': treatmentplan
    }
    return render(request, 'fisiocore/calendar/calendar_day.html', context)
	


  
