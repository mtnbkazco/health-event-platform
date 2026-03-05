import uuid

from fhir.resources.observation import Observation


def create_observation(patient_id):
    value,unit = 120, "mmHg"
    observation_data = {
        "resourceType": "Observation",
        "id": str(uuid.uuid4()),
        "status": "final",  # Mandatory: registered | preliminary | final | amended etc.
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8480-6",
                    "display": "Systolic blood pressure"
                }
            ]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "valueQuantity": {
            "value": value,
            "unit": unit,
            "system": "http://unitsofmeasure.org",
            "code": unit
        }
    }

    return Observation(**observation_data)
