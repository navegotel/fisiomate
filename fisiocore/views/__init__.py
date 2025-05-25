from .patient import patients, view_patient, add_patient, edit_patient, delete_patient
from .examination import examination, add_examination, edit_examination, delete_examination, select_exploration_template, list_exploration_templates, view_exploration_template, add_exploration_template, edit_exploration_template, delete_exploration_template
from .medical_image import add_images, edit_medical_image, delete_medical_image, view_medical_image, imagelist
from .medical_document import view_document, edit_document, add_document, delete_document, document_list
from .import_export import import_file, export_file
from .appointment import view_sessions, add_session, edit_session, delete_session, session_list
from .treatment_plan import view_treatmentplans, add_treatmentplan
from .consent_document import view_consent_documents, view_consent_document, edit_consent_document, delete_consent_document, print_consent_document, add_consent_document, add_consent, view_consents, edit_consent
from .agenda import view_calendar, view_calendar_day
from .dashboard import userprofile, stats
from .misc import protected_download
