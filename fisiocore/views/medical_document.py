import pathlib
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Examination, ClinicalDocument
from ..forms import ClinicalDocumentForm
from ..menu import MAIN_MENU_ITEMS


@login_required
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
    return render(request, 'fisiocore/document/view_medical_document.html', context)


@login_required
def edit_document(request, document_id):
    document = ClinicalDocument.objects.get(pk=document_id)
    if request.method == 'POST':
        form = ClinicalDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_document', args=[document_id]))
    try:
        rendered_form = form.render('fisiocore/document/clinical_document_form.html')
    except NameError:
        form = ClinicalDocumentForm(instance=document)
        rendered_form = form.render('fisiocore/document/clinical_document_form.html')
    context = {
        'title': "Edit Document for {0}".format(document.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'document': document,
        'form': rendered_form
    }
    return render(request, 'fisiocore/document/edit_document.html', context)


@login_required
def add_document(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    context = {
        'title': "Add Document for {0}".format(examination.patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
        'buttonlabel': _('Add document'),
    }
    if request.method == 'POST':
        form = ClinicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination.id]))
    try: 
        rendered_form = form.render('fisiocore/document/clinical_document_form.html')
    except NameError:
        initial_data = {
            'patient': examination.patient.id,
            'examination': examination_id
        }
        form = ClinicalDocumentForm(initial=initial_data)   
        rendered_form = form.render('fisiocore/document/clinical_document_form.html') 
    context['form'] = rendered_form
    return render(request, 'fisiocore/add.html', context)


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
    return render(request, 'fisiocore/document/delete_document.html', context)


@login_required
def document_list(request, patient_id, document_id=None):
    if document_id is None:
        queryset = ClinicalDocument.objects.filter(patient=patient_id)
        if queryset:
            return redirect(reverse('fisiocore:documentlist', args=[patient_id, queryset.latest('creation_date').id]))
    patient = Patient.objects.get(pk=patient_id)
    if document_id is not None:
        document = ClinicalDocument.objects.get(pk=document_id)
    else: 
        document = None
    documents = ClinicalDocument.objects.filter(patient=patient_id)
    context = {
        'title': _("Clinical documents of {0}").format(patient),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'documents': documents,
        'document': document,
    }
    return render(request, 'fisiocore/document/clinical_documents.html', context)

