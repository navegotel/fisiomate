import pathlib
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import InformedConsentDocument, InformedConsent, Patient
from .misc import add_ci_to_context
from ..forms import InformedConsentDocumentForm, InformedConsentForm
from ..menu import MAIN_MENU_ITEMS


@login_required
def view_consent_documents(request):
    consent_documents = InformedConsentDocument.objects.all()
    context = {
        'title': _('Informed consent documents'),
        'main_menu_items': MAIN_MENU_ITEMS,
        'consent_documents': consent_documents
    }
    return render(request, 'fisiocore/informed_consent/view_consent_documents.html', context=context)


@login_required
def view_consent_document(request, consent_id):
    consent_document = InformedConsentDocument.objects.get(pk=consent_id)
    context = {
        'title': _("Informed Consent"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'consent_document': consent_document
    }
    return render(request, 'fisiocore/informed_consent/view_consent_document.html', context=context)


@login_required
def edit_consent_document(request, document_id):
    if request.method == "POST":
        consent_document = InformedConsentDocument.objects.get(pk=document_id)
        form = InformedConsentDocumentForm(request.POST, instance=consent_document)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:view_consent_document', args=[document_id]))
    try:
        consent_document = InformedConsentDocument.objects.get(pk=document_id)
    except InformedConsentDocument.DoesNotExist:
        raise Http404(_("There is no informe consent document with Id {0}").format(document_id))
    form = InformedConsentDocumentForm(instance=consent_document)
    rendered_form = form.render('fisiocore/informed_consent/informed_consent_form.html')
    context = {
        'title': consent_document.title,
        'main_menu_items': MAIN_MENU_ITEMS,
        'consent_document': consent_document,
        'form': rendered_form
    }
    return render(request, 'fisiocore/informed_consent/edit_consent_document.html', context=context)


@login_required
def delete_consent_document(request, document_id):
    consent_document = InformedConsentDocument.objects.get(pk=document_id)
    if request.method == "POST":
        if request.POST.get('confirm') is not None:
            consent_document.delete()
            return redirect(reverse('fisiocore:view_consent_documents'))
    context = {
        'title': _('Delete Informed consent document {0}'.format(consent_document.title)),
        'consent_document': consent_document
    }
    return render(request, 'fisiocore/informed_consent/delete_consent_document.html', context)
    
    

@login_required
def add_consent_document(request):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add Informed consent document",
        'buttonlabel': 'Add document',
        'cancelurl': reverse('fisiocore:view_consent_documents')
    }
    if request.method == "POST":
        form = InformedConsentDocumentForm(request.POST)
        if form.is_valid():
            informed_consent_document = form.save()
            print(informed_consent_document.id)
            return redirect(reverse('fisiocore:view_consent_document', args=[informed_consent_document.id]))
        else:

            rendered_form = form.render('fisiocore/informed_consent/informed_consent_form.html')
            context['form'] = rendered_form
            return render(request, 'add.html', context)
    
    form = InformedConsentDocumentForm(initial={'user': request.user.id})
    rendered_form = form.render('fisiocore/informed_consent/informed_consent_form.html')
    context['form'] = rendered_form
    return render(request, 'add.html', context)
    

def print_consent_document(request, patient_id, document_id):
    patient = Patient.objects.get(pk=patient_id)
    doc = InformedConsentDocument.objects.get(pk=document_id)
    context= {
        'date': datetime.date.today(),
        'patient': patient,
        'doc': doc,
    }
    add_ci_to_context(context)
    return render(request, "fisiocore/informed_consent/print_consent.html", context)




def view_consents(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'title': _("Informed consents"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
    }
    consent_documents = InformedConsentDocument.objects.all()
    unsigned = {}
    for doc in consent_documents:
        unsigned[doc.id] = doc
    consents = InformedConsent.objects.filter(patient = patient_id)
    for consent in consents:
        if consent.revoked is None:
            try:
                unsigned.pop(consent.consent_type.id)
            except KeyError:
                pass
    context['unsigned'] = unsigned
    context['signed'] = consents
        
    return render(request, "fisiocore/informed_consent/view_consents.html", context)
    

def add_consent(request, patient_id, consent_type):
    if request.method == 'POST':
        form = InformedConsentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_consents', args=[patient_id,]))

    if request.method == 'GET': 
        initial_data = {
            'user': request.user.id, 
            'patient': patient_id,
            'consent_type': consent_type,
        }
        form = InformedConsentForm(initial=initial_data)
    rendered_form = form.render('fisiocore/informed_consent/signed_consent_form.html')
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _("Add informed consent"),
        'form': rendered_form,
        'buttonlabel': _("Add informed consent"),
        'cancelurl': reverse('fisiocore:view_consents', args=[patient_id,]),
        'is_upload': True,
    }
    return render(request, "add.html", context)
    
        
    
def edit_consent(request, consent_id):
    consent = InformedConsent.objects.get(pk=consent_id)
    if request.method == 'POST':
        form = InformedConsentForm(request.POST, request.FILES, instance=consent)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocore:view_consents', args=[consent.patient.id,]))
    if request.method == 'GET': 
        form = InformedConsentForm(instance=consent)
        rendered_form = form.render('fisiocore/informed_consent/signed_consent_form.html')
        
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _("Edit informed consent"),
        'form': rendered_form,
        'buttonlabel': _("Edit informed consent"),
        'cancelurl': reverse('fisiocore:view_consents', args=[consent.patient.id,]),
        'is_upload': True,
    }
    return render(request, "add.html", context)
    
    

