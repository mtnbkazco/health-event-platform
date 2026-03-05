import json
from unittest.mock import MagicMock, patch

from persistence_service.canonical_events_consumer import PersistenceService


def create_service():
    with patch("persistence_service.canonical_events_consumer.Consumer"), \
         patch("persistence_service.canonical_events_consumer.Database"):
        service = PersistenceService({}, ["topic"], "db-url")
    service.db = MagicMock()
    service.consumer = MagicMock()
    service.logger = MagicMock()
    return service


def create_message(payload, headers=None):
    message = MagicMock()
    message.value.return_value = payload
    message.headers.return_value = headers or []
    return message


def test_process_event_success():
    service = create_service()
    event = {
        "eventId": "1",
        "tenantId": "tenantA",
        "data": {"resourceType": "Patient"}
    }

    raw = json.dumps(event).encode("utf-8")
    message = create_message(raw, [("trace_id", b"trace123")])
    service.process_event(message, raw)
    service.db.save_resource.assert_called_once()
    service.consumer.commit.assert_called_once()


def test_process_event_invalid_json_logs_error():
    service = create_service()
    raw = b'invalid-json'
    message = create_message(raw)
    service.process_event(message, raw)
    service.logger.error.assert_called()


@patch("persistence_service.canonical_events_consumer.send_to_dlq")
def test_process_event_exception_sends_to_dlq(mock_dlq):
    service = create_service()
    event = {
        "eventId": "1",
        "tenantId": "tenantA",
        "data": {"resourceType": "Condition"}
    }
    raw = json.dumps(event).encode("utf-8")
    message = create_message(raw)
    service.db.save_resource.side_effect = Exception("db failure")
    service.process_event(message, raw)
    mock_dlq.assert_called_once()
    service.consumer.commit.assert_called_once()