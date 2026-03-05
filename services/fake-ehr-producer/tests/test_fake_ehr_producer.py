from unittest.mock import MagicMock, patch
from fake_ehr_producer.ehr_producer import FakeEHRProducer


def test_initialization_sets_topic():
    with patch("fake_ehr_producer.ehr_producer.Producer"):
        producer = FakeEHRProducer(conf={"bootstrap.servers": "localhost:9092"}, topic="raw-events")
    assert producer.topic == "raw-events"


def test_kafka_producer_is_created():
    mock_producer_class = MagicMock()
    with patch("fake_ehr_producer.ehr_producer.Producer", mock_producer_class):
        FakeEHRProducer(conf={"bootstrap.servers": "localhost:9092"}, topic="raw-events")
    mock_producer_class.assert_called_once()