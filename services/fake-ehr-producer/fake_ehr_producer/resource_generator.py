import json
import random
import time
import uuid
from fake_ehr_producer.resources.encounter import create_encounter
from fake_ehr_producer.resources.condition import create_condition
from fake_ehr_producer.resources.observation import create_observation


class BaseGenerator:
    def __init__(self):
        self.tenant = random.choice(["hospitalA", "hospitalB", "hospitalC"])
        self.vendor = random.choice(["EHR_A", "EHR_B", "EHR_C"])
        self.patient_id = uuid.uuid4()
        self.resource_type = random.choice(["ENCOUNTER", "OBSERVATION", "CONDITION"])
        self.resource_status = random.choice(["ACTIVE", "CANCELED", "ERROR", "PROPOSED", "ACCEPTED", "COMPLETE"])


class ResourceGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.resource_type_table = {
            "hospitalA": {"ENCOUNTER": "enc", "OBSERVATION": "obs", "CONDITION": "cond"},
            "hospitalB": {"ENCOUNTER": "ENCOUNTER", "OBSERVATION": "OBSERVATION", "CONDITION": "CONDITION"},
            "hospitalC": {"ENCOUNTER": "ENC", "OBSERVATION": "OBS", "CONDITION": "COND"},
        }

    def generate_payload(self):
        full_payload = {
            "eventId": str(uuid.uuid4()),
            "eventType": self.resource_type_table.get(self.tenant).get(self.resource_type),
            "timestamp": time.time(),
            "tenantId": self.tenant,
            "patientId": str(self.patient_id),
            "source": self.vendor,
            "data": self.fhir_generated_resource()
        }
        return json.dumps(full_payload)

    def fhir_generated_resource(self):
        if self.resource_type in ['ENCOUNTER', 'enc', 'ENC']:
            encounter_obj = create_encounter(self.patient_id).model_dump(mode='json')
            return encounter_obj
        elif self.resource_type in ['CONDITION', 'cond', 'COND']:
            condition_obj = create_condition(self.patient_id).model_dump(mode='json')
            return condition_obj
        else:
            observation_obj = create_observation(self.patient_id).model_dump(mode='json')
            return observation_obj
