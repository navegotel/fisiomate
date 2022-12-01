import pathlib
import calendar
import datetime
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Patient, Examination, MedicalImage, ClinicalDocument, Session
from .forms import PatientForm, ExaminationForm, MedicalImageForm, ClinicalDocumentForm


MAIN_MENU_ITEMS = [
    (_("Patients"), "fisiocore:patients", "fa-home"),
    (_("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (_("Informed consent"), "fisiocore:consents", "fa-pen-alt"),
    (_("Invoicing"), "fisiocore:invoices", "fa-credit-card"),
]

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


FILE_FORMAT = {
    b"\xff\xd8\xff\xe0": "image/jpeg",
    b"\x89\x50\x4e\x47": "image/png",
    b"\x25\x50\x44\x46\x2D": "application/pdf",
}


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
def examination(request, patient_id, examination_id=None):
    if examination_id is None:
        latest = Examination.objects.filter(patient=patient_id).latest('creation_date')
        return redirect(reverse('fisiocore:examination', args=[patient_id, latest.id]))
    patient = Patient.objects.get(pk=patient_id)
    examination = Examination.objects.get(pk=examination_id)
    examination_list = Examination.objects.filter(patient=patient_id)
    images = MedicalImage.objects.filter(examination = examination_id)
    documents = ClinicalDocument.objects.filter(examination = examination_id)
    context = {
        'title': _('Clinical history "{0}"'.format(patient)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'examination_list': examination_list,
        'examination': examination,
        'documents': documents,
        'images': images
    }
    return render(request, 'fisiocore/examination.html', context)


@login_required
def add_examination(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add Examination for {0}".format(patient)
    }
    if request.method == "POST":
        form = ExaminationForm(request.POST)
        if form.is_valid():
            examination = form.save()
            return redirect(reverse('fisiocore:examination', args=[patient_id, examination.id]))
        else:
            rendered_form = form.render('fisiocore/examination_form.html')
            context['form'] = rendered_form
            context['patient_id'] = patient_id
            return render(request, 'fisiocore/add_examination.html', context)
    form = ExaminationForm(initial={'user': request.user.id, 'patient': patient_id})
    rendered_form = form.render('fisiocore/examination_form.html')
    context['form'] = rendered_form
    context['patient_id'] = patient_id
    return render(request, 'fisiocore/add_examination.html', context)
    

@login_required
def edit_examination(request, examination_id):
    if request.method == "POST":
        examination = Examination.objects.get(pk=examination_id)
        form = ExaminationForm(request.POST, instance=examination)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination_id]))
        # return redirect(reverse('fisiocore:examination', args=[examination.patient]))
    try:
        examination = Examination.objects.get(pk=examination_id)
    except Examination.DoesNotExist:
        raise Http404(_("Th    #print(c.monthdays2calendar(year, month))ere is no Examination with Id {0}").format(examination_id))
    if examination.user != request.user:
        raise Http403(_("You are not allowed to see the data of this user"))
    form = ExaminationForm(instance=examination)
    rendered_form = form.render('fisiocore/examination_form.html')
    context = {
        'title': _('Edit Examination "{0}"'.format(examination)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
        'form': rendered_form
    }
    return render(request, 'fisiocore/edit_examination.html', context)


@login_required
def delete_examination(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    patient_id = examination.patient.id
    if request.method == 'POST':
        if request.POST.get('confirm') is not None:
            examination.delete()
            return redirect(reverse('fisiocore:examination', patient_id))
    context = {
        'title': _('Delete examination {0}'.format(examination)),
        'examination': examination
    }
    return render(request, 'fisiocore/delete_examination.html', context)


@login_required
def add_images(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    context = {
        'title': "Add Images for {0}".format(examination.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination
    }
    if request.method == 'POST':
        form = MedicalImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination.id]))
    try: 
        rendered_form = form.render('fisiocore/medical_image_form.html')
    except NameError:
        initial_data = {
            'patient': examination.patient.id,
            'examination': examination_id
        }
        form = MedicalImageForm(initial=initial_data)   
        rendered_form = form.render('fisiocore/medical_image_form.html') 
    context['form'] = rendered_form
    return render(request, 'fisiocore/add_images.html', context)


@login_required
def edit_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    if request.method == 'POST':
        form = MedicalImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_medical_image', args=[image_id]))
    try:
        rendered_form = form.render('fisiocore/medical_image_form.html')
    except NameError:
        form = MedicalImageForm(instance=image)
        rendered_form = form.render('fisiocore/medical_image_form.html')
    context = {
        'title': "Edit Image for {0}".format(image.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'image': image,
        'form': rendered_form
    }
    return render(request, 'fisiocore/edit_image.html', context)


@login_required
def delete_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    if request.method == 'POST':
        if request.POST.get('confirm') is not None:
            image.delete()
            return redirect(reverse('fisiocore:examination', args=[image.patient.id, image.examination.id]))
    context = {
        'title': "Delete image from {0}".format(image.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'image': image,
    }
    return render(request, 'fisiocore/delete_image.html', context)

@login_required
def view_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    context = {
        'title': "View Image for {0}".format(image.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
        'image': image,
    }
    return render(request, 'fisiocore/view_medical_image.html', context)


@login_required
def medical_image(request):
    """open an image from a file on the server and deliver it over http"""
    image_path = pathlib.Path(*pathlib.Path(request.path).parts[2:])
    image_path = conf_settings.MEDIA_ROOT / image_path
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        content_type = FILE_FORMAT.get(image_data[:4])
        if content_type is not None:
            return HttpResponse(image_data, content_type=content_type)
        else:
            raise HttpResponseServerError("Cannot determine content_type")

#@login_required
def document(request):
    """read documente from file on server and return over http"""
    document_path = pathlib.Path(*pathlib.Path(request.path).parts[2:])
    document_path = conf_settings.MEDIA_ROOT / document_path
    with open(document_path, "rb") as doc_file:
        document = doc_file.read()
    return HttpResponse(document, content_type="application/pdf")


@login_required
def view_document(request, document_id):
    document = ClinicalDocument.objects.get(pk=document_id)
    context = {
        'title': "View document for {0}".format(document.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'document': document,
    }
    return render(request, 'fisiocore/view_medical_document.html', context)


@login_required
def edit_document(request, document_id):
    document = ClinicalDocument.objects.get(pk=document_id)
    if request.method == 'POST':
        form = ClinicalDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_document', args=[document_id]))
    try:
        rendered_form = form.render('fisiocore/clinical_document_form.html')
    except NameError:
        form = ClinicalDocumentForm(instance=document)
        rendered_form = form.render('fisiocore/clinical_document_form.html')
    context = {
        'title': "Edit Document for {0}".format(document.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'document': document,
        'form': rendered_form
    }
    return render(request, 'fisiocore/edit_document.html', context)


@login_required
def add_document(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    context = {
        'title': "Add Document for {0}".format(examination.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
    }
    if request.method == 'POST':
        form = ClinicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination.id]))
    try: 
        rendered_form = form.render('fisiocore/clinical_document_form.html')
    except NameError:
        initial_data = {
            'patient': examination.patient.id,
            'examination': examination_id
        }
        form = ClinicalDocumentForm(initial=initial_data)   
        rendered_form = form.render('fisiocore/clinical_document_form.html') 
    context['form'] = rendered_form
    return render(request, 'fisiocore/add_document.html', context)


@login_required
def delete_document(request, document_id):
    document = ClinicalDocument.objects.get(pk=document_id)
    if request.method == 'POST':
        if request.POST.get('confirm') is not None:
            document.delete()
            return redirect(reverse('fisiocore:examination', args=[document.patient.id, document.examination.id]))
    context = {
        'title': "Delete document from {0}".format(document.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'document': document,
    }
    return render(request, 'fisiocore/delete_document.html', context)


@login_required
def imagelist(request, patient_id, image_id=None):
    if image_id is None:
        latest = MedicalImage.objects.filter(patient=patient_id).latest('creation_date')
        if latest is not None:
            return redirect(reverse('fisiocore:imagelist', args=[patient_id, latest.id]))
    patient = Patient.objects.get(pk=patient_id)
    images = MedicalImage.objects.filter(patient=patient_id)
    image = MedicalImage.objects.get(pk=image_id)
    context = {
        'title': _("Clinical images of {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'images': images,
        'image': image,
    }
    return render(request, 'fisiocore/clinical_images.html', context)


@login_required
def document_list(request, patient_id, document_id=None):
    if document_id is None:
        latest = ClinicalDocument.objects.filter(patient=patient_id).latest('creation_date')
        if latest is not None:
            return redirect(reverse('fisiocore:documentlist', args=[patient_id, latest.id]))
    patient = Patient.objects.get(pk=patient_id)
    documents = ClinicalDocument.objects.filter(patient=patient_id)
    document = ClinicalDocument.objects.get(pk=document_id)
    context = {
        'title': _("Clinical documents of {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'documents': documents,
        'document': document,
    }
    return render(request, 'fisiocore/clinical_documents.html', context)


@login_required
def stats(request):
    context = {
        'title': _("Statistics"),
        'main_menu_items': MAIN_MENU_ITEMS,
    }
    return render(request, 'fisiocore/stats.html', context)


@login_required
def userprofile(request):
    context = {
        'title': _("User Profile"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'user': request.user,
    }
    return render(request, 'fisiocore/userprofile.html', context)


@login_required
def session_list(request, patient_id, session_id=None):
    if session_id is None:
        pass

# @login_required
# def medical_image(request):
#     image_path = pathlib.Path(*pathlib.Path(request.path).parts[2:])
#     image_path = conf_settings.MEDIA_ROOT / image_path
#     with open(image_path, "rb") as image_file:
#         image_data = base64.b64encode(image_file.read()).decode('utf-8')
#     context = {
#         'main_menu_items': MAIN_MENU_ITEMS,
#         'title': "View Image",
#         'image': image_data
#     }
#     return render(request, 'fisiocore/show_image.html', context)

    
def view_calendar(request, year=None, month=None):
    if year is None or month is None:
        return redirect(reverse('fisiocore:calendar', args=[datetime.date.today().year, datetime.date.today().month]))
    c = calendar.Calendar()
    current_day = None
    today = datetime.date.today()
    if year == today.year and month == today.month:
        current_day = today.day
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
    sessions = Session.objects.filter(user=request.user, date__year=year, date__month=month)
    context = {
        'title': _(MONTH_NAMES[month]) + ' ' + str(year),
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'month': month,
        'year': year,
        'month_name': _(MONTH_NAMES[month]),
        'prev_month_name': _(MONTH_NAMES[prev_month]),
        'next_month_name': _(MONTH_NAMES[next_month]),
        'main_menu_items': MAIN_MENU_ITEMS,
        'weeks': c.monthdays2calendar(year, month),
        'current_day': current_day,
        'sessions': sessions,
    }
    return render(request, 'fisiocore/calendar_month.html', context)

def view_calendar_day(request, year, month, day):
    date = datetime.date(year, month, day)
    sessions = Session.objects.filter(user=request.user, date=date)
    context={
        'title': date,
        'main_menu_items': MAIN_MENU_ITEMS,
        'sessions': sessions
    }
    return render(request, 'fisiocore/calendar_day.html', context)

def revoke_consent(request, consent_id):
    pass


def consents(request):
    pass
    
    
def add_consent(request):
    pass
    
    
def invoices(request):
    pass
