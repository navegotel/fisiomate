from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from .models import HelpDoc
from pathlib import Path


def main(request, lang=None, page=None):
    if lang is None:
        lang = getattr(settings, "LANGUAGE_CODE")[:2]
    docs = HelpDoc.objects.filter(language = lang)
    context = {
        'docs': docs,
        'lang': lang,
    }
    if page is not None:
        try:
            helpdoc = HelpDoc.objects.get(slug=page)
        except HelpDoc.DoesNotExist:
            raise Http404
        if helpdoc.source_type == 'MD':
            path = getattr(settings, 'DOC_ROOT') / lang /(helpdoc.slug + '.md')
            print(path)
            print(type(path))
            with open(path, 'r') as f:
                content = f.read()
            context['content'] = content
            return render(request, 'fisiohelp/main.html', context)
        elif helpdoc.source_type == 'TMPL':
            return render(request, 'fisiohelp/{0}.html'.format(helpdoc.slug), context)
            
    return render(request, 'fisiohelp/main.html', context)
    
