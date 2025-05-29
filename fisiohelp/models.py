from django.db import models
from django.utils.translation import gettext_lazy as _  

class HelpDoc(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('MD', _('Markdown File')),
        ('TMPL', _('Template File')),
    ]

    source_type = models.CharField(_("Source type"), max_length=4, choices=SOURCE_TYPE_CHOICES, default='MD')
    language = models.CharField(_("Language"), max_length=2)
    subject = models.CharField(_("Subject"), max_length=25)
    slug = models.SlugField(_("Slug"))

    def __str__(self):
        return self.subject
