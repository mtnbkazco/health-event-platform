# TODO - this should be a schema
def validate_event(event_message):
    req_fields = [
        "eventType",
        "timestamp",
        "tenantId",
        "patientId",
        "source",
        "data"
    ]
    for field in req_fields:
        if field not in event_message:
            raise ValueError(f"Missing required field: {field}")

# TODO - FHIR Validation