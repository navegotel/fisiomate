import pathlib
import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

FILE_FORMAT = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89\x50\x4e\x47": "image/png",
    b"\x25\x50\x44\x46\x2D": "application/pdf",
}


def get_file_format(f):
    for fmt in FILE_FORMAT:
        if f.startswith(fmt):
            return FILE_FORMAT[fmt]
    return None
    
    
@login_required
def protected_download(request):
    """read document from file on server and return over http"""
    document_path = pathlib.Path(*pathlib.Path(request.path).parts[2:])
    document_path = settings.MEDIA_ROOT / document_path
    with open(document_path, "rb") as doc_file:
        document = doc_file.read()
    return HttpResponse(document, content_type=get_file_format(document))
    

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

