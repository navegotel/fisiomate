
import io
import json
import datetime
import os
from django.core.files.base import File as DjangoFile
from django.core.files.images import ImageFile
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED
from django.http import HttpResponse
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from .models import Patient, Examination, ClinicalDocument, MedicalImage, Session
import datetime


def import_patient_data(data, zf, user):
    """Create new patient in the database"""
    try:
        patient = Patient(
            user=user,
            last_update=datetime.date.fromisoformat(data['lastUpdate']),
            first_name=data['firstName'],
            last_name=data['lastName'],
            date_of_birth=data['dateOfBirth'],
            city=data['city'],
            post_code=data['postCode'],
            street=data['street'],
            email=data['email'],
            phone=data['phone'],
            id_card_number=data['idCardNumber'],
            habits=data['habits'],
            medical_conditions = data['medical_conditions'],
            remarks=data['remarks'],
            in_treatment=data['inTreatment'],
            )
    except KeyError:
        raise ImportError
    patient.save()
    for examination_data in data['examinations']:
        try:
            examination = Examination(
                user=user,
                last_update=datetime.date.fromisoformat(data['lastUpdate']),
                reason=examination_data['reason'],
                patient=patient,
                interview=examination_data['anamnesis'],
                exploration=examination_data['exploration'],
            )
        except KeyError:
            raise ImportError
        examination.save()
        for document_data in examination_data['clinicalDocuments']:
            b = zf.read(document_data['documentFile'])
            fn = os.path.basename(document_data['documentFile'])
            doc = DjangoFile(io.BytesIO(b), name=fn)
            try:
                clinical_doc = ClinicalDocument(
                    last_update=datetime.date.fromisoformat(document_data['lastUpdate']),
                    patient=patient,
                    examination=examination,
                    label=document_data['label'],
                    upload=doc,
                )
            except (KeyError, ValueError):
                raise ImportError
            clinical_doc.save()

        for image_data in examination_data['medicalImages']:
            print("______________HI_____________")
            b = zf.read(image_data['image'])
            fn = os.path.basename(image_data['image'])
            img = ImageFile(io.BytesIO(b), name=fn)
            try:
                medical_image = MedicalImage(
                    last_update=datetime.date.fromisoformat(image_data['lastUpdate']),
                    patient=patient,
                    examination=examination,
                    image_type=image_data['imageType'],
                    projection=image_data['projection'],
                    description=image_data['description'],
                    image=img,
                )
            except KeyError:
                raise ImportError
            medical_image.save()

    # TODO iterate over examinations
    # TODO introduce images and docs
    print(patient)

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
        d = {   'handle': uuid4().hex,
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
                'habits': p.habits,
                'medical_conditions': p.medical_conditions,
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
                        'description': img.description,
                        'image': img.image.name,
                    }
                )
                filenames.append(img.image.name)
            examinations.append(exam_dict)
        d['examinations'] = examinations
        sessions = []
        for session in p.session_set.all():
            session_dict = {
                'date': session.date.isoformat(),
                'start': session.start.isoformat(),
                'end': session.end.isoformat(),
                'session_number': session.session_number,
                'remarks': session.remarks
            }
            sessions.append(session_dict)
        d['sessions'] = sessions

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