"""
Each main menu item consist of 4 entries:
 - Is sub menu
 - Label
 - Url reverse
 - Icon
"""
from django.utils.translation import gettext_lazy as _


invoicing = [
    (_("Pricing table"), "fisiocash:pricing_table", "fa-table"),
    (_("Invoices"), "fisiocash:invoices", "fa-credit-card"),
    (_("Receipts"), "fisiocash:receipts", "fa-receipt")
]


tools = [
    (_("Import patient data"), "fisiocore:import", "fa-file-import"), 
    (_("Export patient data"), "fisiocore:export", "fa-file-export"), 
    (_("Exploration templates"), "fisiocore:list_exploration_templates", "fa-pen-alt"), 
    (_("Informed consent templates"), "fisiocore:view_consent_documents", "fa-pen-alt")
]


MAIN_MENU_ITEMS = [
    (False, _("Patients"), "fisiocore:patients", "fa-home"),
    (False, _("Calendar"), "fisiocore:calendar", "fa-calendar"),
    (False, _("Invoicing"), "fisiocash:dashboard", "fa-credit-card"),
    (True, _("Tools"), tools, "fa-gear"),
]
