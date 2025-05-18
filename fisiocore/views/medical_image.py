import pathlib
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Examination, MedicalImage
from ..forms import MedicalImageForm
from ..menu import MAIN_MENU_ITEMS


FILE_FORMAT = {
    b"\xff\xd8\xff\xe0": "image/jpeg",
    b"\xff\xd8\xff\xe1": "image/jpeg",
    b"\xff\xd8\xff\xe2": "image/jpeg",
    b"\x89\x50\x4e\x47": "image/png",
    b"\x25\x50\x44\x46\x2D": "application/pdf",
}


@login_required
def add_images(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    context = {
        'title': "Add Images for {0}".format(examination.patient),
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
    return render(request, 'fisiocore/add.html', context)


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
    return render(request, 'fisiocore/add.html', context)


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
    return render(request, 'fisiocore/delete.html', context)

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
def medical_image(request):
    """open an image from a file on the server and deliver it over http"""
    image_path = pathlib.Path(*pathlib.Path(request.path).parts[2:])
    image_path = conf_settings.MEDIA_ROOT / image_path
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        content_type = FILE_FORMAT.get(image_data[:4])
        print(image_data[:4])
        if content_type is not None:
            return HttpResponse(image_data, content_type=content_type)
        else:
            raise HttpResponseServerError("Cannot determine content_type")


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

