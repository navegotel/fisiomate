import pathlib
import base64
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Patient, Examination, MedicalImage, ClinicalDocument
from .forms import PatientForm, ExaminationForm, MedicalImageForm


MAIN_MENU_ITEMS = [
    (_("Patients"), "fisiocore:patients", "fa-home"),
    (_("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (_("Informed consent"), "fisiocore:consents", "fa-pen-alt"),
    (_("Invoicing"), "fisiocore:invoices", "fa-credit-card"),
]


FILE_FORMAT = {
    b"\xff\xd8\xff\xe0": "image/jpeg",
    b"\x89\x50\x4e\x47": "image/png",
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
    patient = Patient.objects.get(pk=patient_id)
    try:
        examination = Examination.objects.get(pk=examination_id)
    except Examination.DoesNotExist:
        examination = None
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
        raise Http404(_("There is no Examination with Id {0}").format(examination_id))
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
        print(request.FILES)
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
    print(form.errors)
    context['form'] = rendered_form
    return render(request, 'fisiocore/add_images.html', context)


@login_required
def edit_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    if request.method == 'POST':
        form = MedicalImageForm(request.POST, instance=image)
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
        pass

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
