
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from ..models import Patient, Session
from ..menu import MAIN_MENU_ITEMS


@login_required
def stats(request):
    p = {}
    p['total'] = Patient.objects.count()
    p['in_treatment'] = Patient.objects.filter(in_treatment=True).count()
    s = {}
    s['year'] = Session.objects.annotate(year = TruncYear("date")).values('year').annotate(count=Count("id"))
    print(s['year'])
    s['month'] = Session.objects.annotate(month = TruncMonth("date")).values('month').annotate(count=Count("id"))
    context = {
        'title': _("Statistics"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patients' : p,
        'sessions': s
    }
    return render(request, 'fisiocore/view_stats.html', context)


@login_required
def userprofile(request):
    context = {
        'title': _("User Profile"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'user': request.user,
    }
    return render(request, 'fisiocore/userprofile.html', context)
