from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from ..models import Patient, Examination, MedicalImage, ClinicalDocument, ExplorationTemplate
from ..forms import ExaminationForm, ExplorationTemplateForm 
from ..menu import MAIN_MENU_ITEMS
    
    
@login_required
def examination(request, patient_id, examination_id=None):
    if examination_id is None:
        queryset = Examination.objects.filter(patient=patient_id)
        if queryset:
            return redirect(reverse('fisiocore:examination', args=[patient_id, queryset.latest('creation_date').id]))
    patient = Patient.objects.get(pk=patient_id)
    if examination_id is not None:
        examination = Examination.objects.get(pk=examination_id)
    else: 
        examination = None
    examination_list = Examination.objects.filter(patient=patient_id)
    images = MedicalImage.objects.filter(examination = examination_id)
    documents = ClinicalDocument.objects.filter(examination = examination_id)
    context = {
        'title': _('Clinical history'),
        'main_menu_items': MAIN_MENU_ITEMS,
        'patient': patient,
        'examination_list': examination_list,
        'examination': examination,
        'documents': documents,
        'images': images
    }
    return render(request, 'fisiocore/examination/view_examination.html', context)


@login_required
def add_examination(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Add Examination"
    }
    if request.method == "POST":
        form = ExaminationForm(request.POST)
        if form.is_valid():
            examination = form.save()
            return redirect(reverse('fisiocore:examination', args=[patient_id, examination.id]))
        else:
            rendered_form = form.render('fisiocore/examination/examination_form.html')
            context['form'] = rendered_form
            context['patient_id'] = patient_id
            return render(request, 'fisiocore/add.html', context)
    try:
        exploration_template = ExplorationTemplate.objects.get(pk=request.GET["tmpl"])
        exploration = exploration_template.exploration
        interview = exploration_template.anamnesis
    except KeyError:
        exploration = ""
        interview = ""

    form = ExaminationForm(initial={'user': request.user.id, 
                                    'patient': patient_id,
                                    'exploration': exploration,
                                    'interview': interview,
                                    }
                            )
    rendered_form = form.render('fisiocore/examination/examination_form.html')
    context['form'] = rendered_form
    context['patient_id'] = patient_id
    return render(request, 'fisiocore/examination/add_examination.html', context)
    

@login_required
def edit_examination(request, examination_id):
    if request.method == "POST":
        examination = Examination.objects.get(pk=examination_id)
        form = ExaminationForm(request.POST, instance=examination)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:examination', args=[examination.patient.id, examination_id]))
    try:
        examination = Examination.objects.get(pk=examination_id)
    except Examination.DoesNotExist:
        raise Http404(_("There is no Examination with Id {0}").format(examination_id))
    if examination.user != request.user:
        raise Http403(_("You are not allowed to see the data of this user"))
    form = ExaminationForm(instance=examination)
    rendered_form = form.render('fisiocore/examination/examination_form.html')
    context = {
        'title': _('Edit Examination'),
        'main_menu_items': MAIN_MENU_ITEMS,
        'examination': examination,
        'form': rendered_form
    }
    return render(request, 'fisiocore/examination/edit_examination.html', context)


@login_required
def delete_examination(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    patient_id = examination.patient.id
    if request.method == 'POST':
        if request.POST.get('confirm') is not None:
            examination.delete()
            return redirect(reverse('fisiocore:examination', args=[patient_id]))
    context = {
        'title': _('Delete examination {0}'.format(examination)),
        'examination': examination
    }
    return render(request, 'fisiocore/examination/delete_examination.html', context)


@login_required
def select_exploration_template(request, patient_id):
    exploration_template_list = ExplorationTemplate.objects.all()
    context = {
        'title': _('select examination template'),
        'exploration_template_list': exploration_template_list,
        'patient_id': patient_id
    }
    return render(request, "fisiocore/examination_template/select_examination_template.html", context)


@login_required
def list_exploration_templates(request):
    exploration_templates = ExplorationTemplate.objects.all()
    context = {
        'title': _("Exploration Templates"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'exploration_templates': exploration_templates
    }
    return render(request, 'fisiocore/examination_template/list_examination_templates.html', context)



@login_required
def view_exploration_template(request, tmpl_id):
    exploration_template = ExplorationTemplate.objects.get(pk=tmpl_id)
    context = {
        'title': exploration_template.title,
        'main_menu_items': MAIN_MENU_ITEMS,
        'exploration_template': exploration_template,
    }
    return render(request, 'fisiocore/examination_template/view_examination_template.html', context)


@login_required
def add_exploration_template(request):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': 'New exploration template',
        'buttonlabel': 'Add template',
        'cancelurl': reverse('fisiocore:list_exploration_templates')
    }
    if request.method == "POST":
        form = ExplorationTemplateForm(request.POST)
        if form.is_valid():
            exploration_template = form.save()
            return redirect(reverse('fisiocore:view_exploration_template', args=[exploration_template.id]))
        else:
            rendered_form = form.render('fisiocore/examination_template/examination_template_form.html')
            context['form'] = rendered_form
            return render(request, 'fisiocore/examination_template/add_examination_template.html', context)
    form = ExplorationTemplateForm(initial={'user':request.user.id})
    rendered_form = form.render('fisiocore/examination_template/examination_template_form.html')
    context['form'] = rendered_form
    return render(request, 'fisiocore/add.html', context)


@login_required
def edit_exploration_template(request, tmpl_id):
    if request.method == "POST":
        exploration_template = ExplorationTemplate.objects.get(pk=tmpl_id)
        form = ExplorationTemplateForm(request.POST, instance=exploration_template)
        if form.is_valid():
            form.save()
        return redirect(reverse('fisiocore:view_exploration_template', args=[exploration_template.id]))
    try:
        exploration_template = ExplorationTemplate.objects.get(pk=tmpl_id)
    except ExplorationTemplate.DoesNotExist:
        raise Http404(_("There is no exploration template with Id {0}").format(tmpl_id))
    form = ExplorationTemplateForm(instance=exploration_template)
    rendered_form = form.render('fisiocore/examination_template/examination_template_form.html')
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': "Edit exploration template",
        'exploration_template': exploration_template,
        'form': rendered_form
    }
    return render(request, 'fisiocore/examination_template/edit_examination_template.html', context=context)


def delete_exploration_template(request, tmpl_id):
    exploration_template = ExplorationTemplate.objects.get(pk=tmpl_id)
    if request.method == "POST":
        if request.POST.get('confirm') is not None:
            exploration_template.delete()
            return redirect(reverse('fisiocore:list_exploration_templates'))
    context = {
        'title': _('delete exploration template'),
        'are_you_sure_msg': _('Are you sure you want to delete the exploration template "{0}"?').format(exploration_template.title),
        'cancel_url': reverse('fisiocore:view_exploration_template', args=[tmpl_id])
    }
    return render(request, 'fisiocore/delete.html', context)

    

