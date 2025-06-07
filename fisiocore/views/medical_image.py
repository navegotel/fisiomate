from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Examination, MedicalImage
from ..forms import MedicalImageForm
from ..menu import MAIN_MENU_ITEMS
from .misc import get_file_format


@login_required
def add_images(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    context = {
        'title': _("Add image"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
        'buttonlabel': _('Add image'),
        'is_upload': True,
    }
    if request.method == 'POST':
        form = MedicalImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination.id]))
    try: 
        rendered_form = form.render('fisiocore/medical_image/medical_image_form.html')
    except NameError:
        initial_data = {
            'patient': examination.patient.id,
            'examination': examination_id
        }
        form = MedicalImageForm(initial=initial_data)   
        rendered_form = form.render('fisiocore/medical_image/medical_image_form.html') 
    context['form'] = rendered_form
    return render(request, 'add.html', context)


@login_required
def edit_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    if request.method == 'POST':
        form = MedicalImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_medical_image', args=[image_id]))
    try:
        rendered_form = form.render('fisiocore/medical_image/medical_image_form.html')
    except NameError:
        form = MedicalImageForm(instance=image)
        rendered_form = form.render('fisiocore/medical_image/medical_image_form.html')
    context = {
        'title': "Edit Image for {0}".format(image.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'image': image,
        'form': rendered_form,
        'buttonlabel': _('Save image'),
    }
    return render(request, 'add.html', context)


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
        'are_you_sure_msg': "Are you sure you want to delete this image from patient {0} {1}".format(image.patient.first_name, image.patient.last_name),
        'cancel_url': reverse('fisiocore:view_medical_image', args=[image_id])
    }
    return render(request, 'delete.html', context)

@login_required
def view_medical_image(request, image_id):
    image = MedicalImage.objects.get(pk=image_id)
    context = {
        'title': "View Image for {0}".format(image.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': image.examination,
        'image': image,
    }
    return render(request, 'fisiocore/medical_image/view_medical_image.html', context)


@login_required
def imagelist(request, patient_id, image_id=None):
    if image_id is None:
        queryset = MedicalImage.objects.filter(patient=patient_id)
        if queryset:
            return redirect(reverse('fisiocore:imagelist', args=[patient_id, queryset.latest('creation_date').id]))
    patient = Patient.objects.get(pk=patient_id)
    if image_id is not None:
        image = MedicalImage.objects.get(pk=image_id)
    else:
        image = None
    images = MedicalImage.objects.filter(patient=patient_id)
    context = {
        'title': _("Clinical images of {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'images': images,
        'image': image,
    }
    return render(request, 'fisiocore/medical_image/medical_images.html', context)

