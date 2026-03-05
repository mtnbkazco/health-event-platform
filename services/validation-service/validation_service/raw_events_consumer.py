import json
import os
import uuid

from confluent_kafka import Consumer, Producer
from validation_service.dlq_producer import send_to_dlq
from validation_service.validation import validate_schema
from services.config.logger_config import get_logger, trace_id
from services.config import env_loader


class ValidationService:
    def __init__(self, consumer_conf, consumer_subscribe, producer_conf, producer_topic):
        self.logger = get_logger("validation-service")
        self.consumer = Consumer(consumer_conf)
        self.consumer.subscribe(consumer_subscribe)
        self.producer = Producer(producer_conf)
        self.producer_topic = producer_topic

    def start(self):
        self.logger.info("ValidationService service started, waiting for messages...")
        try:
            while True:
                message = self.consumer.poll(2.0)
                if message is None:
                    continue

                if message.error():
                    self.logger.error(f"Error: {message.error()}")
                    continue

                raw_data = message.value()
                if not raw_data:
                    self.logger.info("Skipping empty message...")
                    continue

                self.process_event(message, raw_data)
        except KeyboardInterrupt:
            self.logger.info("Shutdown signal received...")
        finally:
            self.logger.info("cleaning up connections")
            self.producer.flush(timeout=10)
            self.consumer.close()

    def process_event(self, message, raw_data):
        try:
            decode_data = raw_data.decode("utf-8")
            event = json.loads(decode_data)
            # try to validate event
            validate_schema(event)
            # extract headers to carry over trace id
            headers = message.headers() or []
            header_dict = { k: v.decode('utf-8') for k, v in headers}
            # get incoming trace id
            extracted_trace_id = header_dict.get('trace_id') or str(uuid.uuid4())
            trace_id.set(extracted_trace_id)
            self.producer.produce(
                topic=self.producer_topic,
                key=message.key(),
                headers=[("trace_id", trace_id.get().encode('utf-8'))],
                value=json.dumps(event)
            )
            self.producer.poll(0) # clear internal queue

            self.consumer.commit(message=message)
            self.logger.info(
                f"Received, validated and processed event: {event}",
                     extra={
                         "event_id": event["eventId"],
                         "tenant": event["tenantId"],
                         "trace_id": trace_id.get()
                     }
                )

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e} | Raw data: {decode_data}")
        except Exception as e:
            self.logger.error(f"Exception has occurred: {e}")
            send_to_dlq(message, str(e))
            self.consumer.commit(message=message)


if __name__ == "__main__":
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    consumer_conf = {
        'bootstrap.servers': kafka_server,
        'group.id': 'raw-clinical-events-group',
        'auto.offset.reset': 'earliest',
        'max.poll.interval.ms': 300000
    }
    consumer_subscribe = ["raw-clinical-events"]

    # producer to emit to normalization
    producer_conf = {
        'bootstrap.servers': kafka_server
    }
    producer_topic = "normalize-clinical-events"
    svc = ValidationService(consumer_conf, consumer_subscribe, producer_conf, producer_topic)
    svc.start()