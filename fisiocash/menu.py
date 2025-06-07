from django.utils.translation import gettext_lazy as _

invoices = [
    (_("Per Month"), "fisiocash:invoices", "fa-calendar"),
    (_("Per Patient"), "fisiocash:invoices_by_patient", "fa-user"),
]

quotes = [
    (_("Per Month"), "fisiocash:quotes", "fa-calendar"),
    (_("Per Patient"), "fisiocash:quotes_by_patient", "fa-user"),
]

MAIN_MENU_ITEMS = [
    (False, _("Clínic"), "fisiocore:patients", "fa-home"),
    (True, _("Quotes"), quotes, "fa-table"),
    (True, _("Invoices"), invoices, "fa-credit-card"),
    (False, _("Price list"), "fisiocash:pricelist", "fa-table"),
]
