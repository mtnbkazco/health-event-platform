import uuid

from fhir.resources.R4B.condition import Condition
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

def create_condition(patient_id):
    condition_data = {
        "resourceType": "Condition",
        "id": str(uuid.uuid4()),
        # clinicalStatus is mandatory in most profiles
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org",
                    "code": "active"
                }
            ]
        },
        # subject links the condition to your patient
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        # The actual diagnosis code
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info",
                    "code": "38341003",
                    "display": "Essential hypertension"
                }
            ],
            "text": "Essential hypertension"
        }
    }

    return Condition(**condition_data)