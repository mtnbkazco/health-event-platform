import json

from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9092'
}
dql_producer = Producer(conf)

topic = "normalize-clinical-events-dql"

def send_to_dlq(event_message, error):
    """sends the raw FAILED message plus metadata about the error"""
    # Use headers to store the error so the payload stays clean FHIR
    headers = [
        ("error_reason", str(error).encode('utf-8')),
        ("original_topic", event_message.topic().encode('utf-8'))
    ]
    payload = {
        "original_message": event_message.value().decode('utf-8'),
        "error": str(error),
        "topic": event_message.topic(),
        "partition": event_message.partition(),
        "offset": event_message.offset()
    }
    dql_producer.produce(
        topic,
        value=json.dumps(payload),
        headers=headers
    )
    dql_producer.flush()