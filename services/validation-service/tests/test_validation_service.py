import datetime
import time
import uuid

import pytest
from jsonschema.exceptions import ValidationError

from validation_service.validation import validate_schema


def test_valid_event_passes():
    event = {
        "eventId": str(uuid.uuid4()),
        "eventType": "observation",
        "patientId": "p1",
        "tenantId": "some-hospital",
        "timestamp": time.time(),
        "source": "EHR-X",
        "data": { "resourceType": "Condition", "id": "12345678" }
    }
    result = validate_schema(event)

    assert result is None # none means schema is valid


def test_missing_patient_id_fails():
    event = {
        "eventId": str(uuid.uuid4()),
        "eventType": "observation",
        "tenantId": "some-hospital",
        "timestamp": time.time(),
        "source": "EHR-X",
        "data": { "resourceType": "Condition", "id": "12345678" }
    }
    with pytest.raises(ValidationError):
        validate_schema(event)


def test_invalid_event_type_fails():
    event = {
        "eventId": str(uuid.uuid4()),
        "patientId": "p1",
        "eventType": None,
        "tenantId": "some-hospital",
        "timestamp": time.time(),
        "source": "EHR-X",
        "data": { "resourceType": "Condition", "id": "12345678" }
    }

    with pytest.raises(ValidationError):
        validate_schema(event)