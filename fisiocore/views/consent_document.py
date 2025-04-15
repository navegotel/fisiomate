from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import InformedConsentDocument
from ..forms import InformedConsentDocumentForm
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
def view_consent_document(request, document_id):
    consent_document = InformedConsentDocument.objects.get(pk=document_id)
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
        'title': "Add Informed consent document"
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
            return render(request, 'fisiocore/informed/consent/add_informed_consent.html', context)
    
    form = InformedConsentDocumentForm(initial={'user': request.user.id})
    rendered_form = form.render('fisiocore/informed_consent/informed_consent_form.html')
    context['form'] = rendered_form
    return render(request, 'fisiocore/informed_consent/add_informed_consent.html', context)


def view_consent(request, patient_id, consent_id=None):
    pass
    
    
def add_consent(request, patient_id, consent_template_id):
    pass
    
    
def revoke_consent(request, consent_id):
    pass
