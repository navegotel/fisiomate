from django import template

register = template.Library()

@register.filter
def invoice_nbr(value):
    try:
        return "{:06d}".format(value)
    except (ValueError, TypeError):
        return value
