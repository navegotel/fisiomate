import zipfile
import json
from uuid import uuid4
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _
from ..imex import import_patient_data, export_patient_data
from ..models import Patient
from ..menu import MAIN_MENU_ITEMS


@login_required
def import_file(request):
    context = {
        'title': _("Import Patient Data"),
        'main_menu_items': MAIN_MENU_ITEMS,
    }
    if request.method == "POST":
        token = request.POST.get('transaction_token') 
        if token is None or len(token) == 0:
            uploaded_file = request.FILES.get('upload')
            with zipfile.ZipFile(uploaded_file, mode='r') as zf:
                try:
                    m = zf.read("manifest.json")
                    context['manifest'] = json.loads(m)
                    pd = zf.read("data.json")
                    context['patient_data'] = json.loads(pd)
                except KeyError:
                    context["errormsg"] = _("This zip file does not seem to contain valid patient data.")
                    return render(request, 'fisiocore/imex/import.html', context)
            context['transaction_token'] = uuid4().hex
            FileSystemStorage(location=conf_settings.TEMPDIR).save("{0}.zip".format(context['transaction_token']), uploaded_file)
            return render(request, 'fisiocore/imex/import.html', context)
        else:
            importgroup = request.POST.getlist('importgroup')
            tf = FileSystemStorage(location=conf_settings.TEMPDIR).open("{0}.zip".format(request.POST.get('transaction_token')))
            with zipfile.ZipFile(tf, mode='r') as zf:
                ds = zf.read("data.json")
                pd = json.loads(ds)
                for patient in pd:
                    if patient['handle'] in importgroup:
                        try:
                            import_patient_data(patient, zf, request.user)
                        except ImportError:
                            pass
                            # TODO Needs to be handled gracefully
            return redirect(reverse('fisiocore:patients'))
                    
    if request.method == "GET":
        return render(request, 'fisiocore/imex/import.html', context)


@login_required
def export_file(request):
    if request.method == "POST":
        items = request.POST.getlist('export')
        if request.POST.get("basiconly") == "on":
            include_examination_data=False
        else:
            include_examination_data=True
        return export_patient_data(
            [int(x) for x in items], 
            request.user, 
            include_examination_data=include_examination_data
        )

    if request.method == "GET":
        patients = Patient.objects.filter(user=request.user)
        context = {
            'title': _("Export Patient Data"),
            'main_menu_items': MAIN_MENU_ITEMS,
            'patients': patients,
        }
        return render(request, 'fisiocore/imex/export.html', context)
