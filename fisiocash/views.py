import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .menu import MAIN_MENU_ITEMS
from .models import ListPrice, Quote
from .forms import ListPriceForm


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
    }
    return render(request, 'fisiocash/quotes_by_month.html', context)
    
    
def quotes_by_patient(request, patient_id):
    pass
    

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
            rendered_form = form.render('fisiocash/price_form.html')
            context['form'] = rendered_form
            return render(request, 'add.html', context)
    form = ListPriceForm(initial={'user':request.user.id})
    rendered_form = form.render('fisiocash/price_form.html')
    context['form'] = rendered_form
    return render(request, 'add.html', context)
    

def edit_price(request, price_id):
    price = ListPrice.objects.get(pk=price_id)
    if request.method == "POST":
        form = ListPriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect(reverse('fisiocash:view_price', args=[price_id]))
    try:
        rendered_form = form.render('fisiocash/price_form.html')
    except NameError:
        form = ListPriceForm(instance=price)
        rendered_form = form.render('fisiocash/price_form.html')
    context = {
        'main_menu_items': MAIN_MENU_ITEMS,
        'title': _('Edit price'),
        'form': rendered_form,
        'currency': getattr(settings, "CURRENCY"),
        'buttonlabel': _('Save price'),
    }
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

