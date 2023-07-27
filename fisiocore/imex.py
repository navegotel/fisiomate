
import io
import json
import datetime
import os
from zipfile import ZipFile, ZIP_DEFLATED
from django.http import HttpResponse
from django.conf import settings
from .models import Patient


def import_patient_data(data):
    pass

def get_manifest(user):
    manifest = {
        'exportDate': datetime.date.today().isoformat(),
        'user': "{0} {1}".format(user.first_name, user.last_name),
        'email': user.email,
        'version': settings.VERSION
    }
    return json.dumps(manifest, indent=4, ensure_ascii=False)

def export_patient_data(patient_ids, user, include_examination_data=True):
    filenames = []
    l = []
    for patient_id in patient_ids:
        p = Patient.objects.get(pk=patient_id)
        d = {
                'lastUpdate': p.last_update.isoformat(),
                'firstName': p.first_name,
                'lastName': p.last_name,
                'dateOfBirth': p.date_of_birth.isoformat(),
                'city': p.city,
                'postCode': p.post_code,
                'street': p.street,
                'email': p.email,
                'phone': p.phone,
                'idCardNumber': p.id_card_number,
                'remarks': p.remarks,
                'inTreatment': p.in_treatment,
            }
        if include_examination_data is False:
            l.append(d)
            continue
        examinations = []
        for examination in p.examination_set.all():
            exam_dict = {
                'lastUpdate': examination.last_update.isoformat(),
                'reason': examination.reason,
                'anamnesis': examination.interview,
                'exploration': examination.exploration,
                'clinicalDocuments': [],
                'medicalImages': [],
            }
            for document in examination.clinicaldocument_set.all():
                exam_dict['clinicalDocuments'].append(
                    {
                        'lastUpdate': document.last_update.isoformat(),
                        'label': document.label,
                        'documentFile': document.upload.name,
                    }
                )
                filenames.append(document.upload.name)
            for img in examination.medicalimage_set.all():
                exam_dict['medicalImages'].append(
                    {
                        'lastUpdate': img.last_update.isoformat(),
                        'imageType': img.image_type,
                        'projection': img.projection,
                        'descriptions': img.description,
                        'image': img.image.name,
                    }
                )
                filenames.append(img.image.name)
            examinations.append(exam_dict)
        d['examinations'] = examinations

        l.append(d)
    buf = io.BytesIO()
    with ZipFile(buf, "w") as z:
        z.writestr("data.json", json.dumps(l, indent=4, ensure_ascii=False), compress_type=ZIP_DEFLATED)
        z.writestr("manifest.json", get_manifest(user), compress_type=ZIP_DEFLATED)
        for filename in filenames:
            z.write(os.path.join(settings.MEDIA_ROOT, filename), filename, compress_type=ZIP_DEFLATED)
    response = HttpResponse(buf.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=export_{0}".format(datetime.date.today().isoformat())
    return response