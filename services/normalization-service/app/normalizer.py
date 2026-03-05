from datetime import datetime

from app.mapper import FhirResourceMap

def normalize_event(event):
    raw_type = event["eventType"]
    event_type = FhirResourceMap.from_event_type(raw_type)

    if not event_type:
        raise ValueError(f"Unknown eventType: {raw_type}")

    event["eventType"] = event_type
    event["originalEventType"] = raw_type
    event["normalizedAt"] = datetime.now().isoformat()
    return event


