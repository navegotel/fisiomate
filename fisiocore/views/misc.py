import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from ..models import Patient, Session
from ..menu import MAIN_MENU_ITEMS


def add_ci_to_context(context):
    context['logo'] = getattr(settings, "LOGO")
    context['brand_name'] = getattr(settings, "BRAND_NAME")
    context['legal_name'] = getattr(settings, "LEGAL_NAME")
    context['address_line_1'] = getattr(settings, "ADDRESS_LINE_1")
    context['address_line_2'] = getattr(settings, "ADDRESS_LINE_2")
    context['address_line_3'] = getattr(settings, "ADDRESS_LINE_3")
    context['address_line_4'] = getattr(settings, "ADDRESS_LINE_4")
    context['tax_number'] = getattr(settings, "TAX_NUMBER")
    context['phone'] = getattr(settings, "PHONE")
    context['email'] = getattr(settings, "EMAIL")
    context['website'] = getattr(settings, "WEBSITE")
    context['account_number'] = getattr(settings, "ACCOUNT_NUMBER")
    context['place'] = getattr(settings, 'PLACE')

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
