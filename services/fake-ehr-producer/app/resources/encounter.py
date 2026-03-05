import uuid

from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.period import Period
from datetime import datetime, timezone


def create_encounter(patient_id):
    patient_ref = Reference(**{
        "reference": f"Patient/{patient_id}",
        "display": "John B. Anyperson"
    })

    # 2. Define the status of the encounter
    encounter_status = "finished"

    # 3. Define the encounter class (e.g., ambulatory)
    encounter_class = Coding(**{
        "system": "http://terminology.hl7.org",
        "code": "AMB",
        "display": "Ambulatory"
    })

    # 4. Define the encounter type (e.g., a specific checkup)
    encounter_type = CodeableConcept(**{
        "coding": [
            Coding(**{
                "system": "http://snomed.info",
                "code": "185349003",
                "display": "Encounter for check up"
            })
        ]
    })

    # 5. Define the period of the encounter
    encounter_period = Period(**{
        "start": datetime.now(timezone.utc).isoformat(),
        "end": datetime.now(timezone.utc).isoformat()
    })

    # 6. Create the Encounter resource instance using the imported class
    encounter = Encounter(**{
        "id": str(uuid.uuid4()),
        "status": encounter_status,
        "class_fhir": encounter_class, # Use 'class_fhir' to avoid Python keyword conflict
        "subject": patient_ref,
        "type": [encounter_type],
        "period": encounter_period
    })
    return encounter