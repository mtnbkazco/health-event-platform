import json
from pathlib import Path

from jsonschema import validate

SCHEMA_PATH = Path(__file__).resolve().parent / "schema" / "v1" / "canonical_event_schema.json"
with open(SCHEMA_PATH) as f:
    SCHEMA = json.load(f)


def validate_schema(event_message):
    validate(instance=event_message, schema=SCHEMA)


# TODO - FHIR Validation
