from normalization_service.normalizer import normalize_event


def test_normalizes_code_system():
    event = {
        "eventType": "obs",
        "traceId": "abc",
        "patientId": "p1",
        "code": "BP_SYS",
        "value": 120
    }

    normalized = normalize_event(event)

    assert normalized["eventType"] == "Observation"
    assert normalized["traceId"] == "abc"
    assert normalized["originalEventType"] == "obs"


def test_preserves_trace_id():
    event = {
        "eventType": "CONDITION",
        "traceId": "trace-1",
        "patientId": "p1",
        "code": "8480-6",
        "value": 120
    }

    normalized = normalize_event(event)

    assert normalized["eventType"] == "Condition"
    assert normalized["originalEventType"] == "CONDITION"
    assert normalized["traceId"] == "trace-1"