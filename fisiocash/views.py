import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .menu import MAIN_MENU_ITEMS
from .models import ListPrice, Quote
from .forms import ListPriceForm, QuoteForm
from fisiocore.models import Patient


def invoices(request):
    t = datetime.date.today()
    return redirect(reverse('fisiocash:invoices_by_month', args=[t.year, t.month]))
    
    
def quotes(request):
    t = datetime.date.today()
    return redirect(reverse('fisiocash:quotes_by_month', args=[t.year, t.month]))


def dashboard(request):
    context = {
        'title': _("Overview"),
        'main_menu_items': MAIN_MENU_ITEMS,
    }
    return render(request, 'fisiocash/dashboard.html', context)


def session_create_or_show_quote(request, session_id):
    context = {
        'title': _("Quote"),
        'main_menu_items': MAIN_MENU_ITEMS,
    }
    return render(request, 'fisiocash/quotes_by_month.html', context)


def add_quote(request, patient_id=None):
    if request.method == "POST":
        print(request.POST)
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            return redirect(reverse('fisiocash:edit_quote', args=[quote.id]))
    form = QuoteForm(initial={'user':request.user.id})
    #TODO
    # print(formset.render('fisiocash/quote_item_form.html'))
    context = {
        'title': _("Quote"),
        'main_menu_items': MAIN_MENU_ITEMS,
        'form': form
    }
    return render(request, 'add.html', context)
    

def edit_quote(request, quote_id):
    pass

def quotes_by_month(request, year, month):
    months = Quote.objects.dates('date', 'month')
    quotes = Quote.objects.filter(date__year=year).filter(date__month=month)
    context = {
        'title': _("Quotes for {0} / {1}".format(month, year)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'months': months,
        'quotes': quotes,
        'active_month': month,
        'active_year': year,
        'currency': getattr(settings, "CURRENCY")
    }
    return render(request, 'fisiocash/quotes_by_month.html', context)
   
def quotes_by_patient_without_patient_id(request):
    patient = Patient.objects.first()
    return redirect(reverse('fisiocash:quotes_by_patient', args=[patient.id]))
    
def quotes_by_patient(request, patient_id):
    patients = Patient.objects.filter(quote__isnull=False).distinct()
    patient = Patient.objects.get(pk=patient_id)
    quotes = patient.quote_set.all()
    context = {
        'title': _("Quotes for {0} / {1}".format(patient.first_name, patient.last_name)),
        'main_menu_items': MAIN_MENU_ITEMS,
        'currency': getattr(settings, "CURRENCY"),
        'patient': patient,
        'patients': patients,
        'quotes': quotes,
    }
    return render(request, 'fisiocash/quotes_by_patient.html', context)
    

def invoices_by_month(request, year=None, month=None):
    pass
    
    
def invoices_by_patient(request, patient_id=None):
    pass
    
    
def pricelist(request):
    prices = ListPrice.objects.all()
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _('Prices'),
        'prices': prices,
        'currency': getattr(settings, "CURRENCY")
    }
    return render(request, 'fisiocash/prices.html', context)
    
def add_price(request):
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _('Add price'),
        'currency': getattr(settings, "CURRENCY"),
        'buttonlabel': _('Add price'),
    }
    if request.method == 'POST':
        form = ListPriceForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect(reverse('fisiocash:pricelist'))
        else:
            context['form'] = form
            return render(request, 'add.html', context)
    context['form'] = ListPriceForm(initial={'user':request.user.id})
    return render(request, 'add.html', context)
    

def edit_price(request, price_id):
    price = ListPrice.objects.get(pk=price_id)
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _('Edit price'),
        'currency': getattr(settings, "CURRENCY"),
        'buttonlabel': _('Save price'),
    }
    if request.method == "POST":
        form = ListPriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocash:view_price', args=[price_id]))
        else:
            context['form'] = form
            return render(request, 'add.html', context)

    context['form'] = ListPriceForm(instance=price)
    return render(request, 'add.html', context)

    
def view_price(request, price_id):
    listprice = ListPrice.objects.get(pk=price_id)
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _('List price'),
        'currency': getattr(settings, "CURRENCY"),
        'listprice': listprice
    }
    return render(request, 'fisiocash/view_price.html', context)
    
    

# def show_invoice_template(request):
    # context = {
        # 'title': _('Invoice'),
        # 'document_type': _('Invoice'),
        # 'logo': conf_settings.LOGO,
        # 'brand_name': conf_settings.BRAND_NAME,
        # 'legal_name': conf_settings.LEGAL_NAME,
        # 'address_line_1': conf_settings.ADDRESS_LINE_1,
        # 'address_line_2': conf_settings.ADDRESS_LINE_2,
        # 'address_line_3': conf_settings.ADDRESS_LINE_3,
        # 'address_line_4': conf_settings.ADDRESS_LINE_4,
        # 'tax_number': conf_settings.TAX_NUMBER,
        # 'phone': conf_settings.PHONE,
        # 'email': conf_settings.EMAIL,
        # 'website': conf_settings.WEBSITE,
        # 'account_number': conf_settings.ACCOUNT_NUMBER,
        # 'invoice_date': datetime.date.today(),
        # 'invoice_number': "XXXXXX",


    # }
    # return render(request, "fisiocore/print/base.html", context)

