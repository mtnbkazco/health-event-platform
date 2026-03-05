import json
import os

from confluent_kafka import Consumer

from app.database import Database
from app.dlq_producer import send_to_dlq
from services.config.logger_config import get_logger, trace_id


class PersistenceService:
    def __init__(self, consumer_conf, consumer_subscribe, db_url):
        self.logger = get_logger("persistence-service")
        self.consumer = Consumer(consumer_conf)
        self.consumer.subscribe(consumer_subscribe)
        self.db = Database(db_url)

    def start(self):
        self.logger.info("PersistenceService service started, waiting for messages...")
        try:
            while True:
                message =self.consumer.poll(2.0)

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
            self.consumer.close()
            self.db.disconnect()

    def process_event(self, message, raw_data):
        try:
            decode_data = raw_data.decode("utf-8")
            event = json.loads(decode_data)

            headers = message.headers() or []
            header_dict = {k: v.decode('utf-8') for k, v in headers}
            current_trace = header_dict.get('trace_id', "UNKNOWN")
            trace_id.set(current_trace)
            self.db.save_resource(event['data']['resourceType'], event, trace_id.get())
            self.consumer.commit(message=message, asynchronous=False)
            self.logger.info(
                f"Event written to db: {event}",
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
        'group.id': 'canonical-service-group',
        'auto.offset.reset': 'earliest',
        'max.poll.interval.ms': 300000
    }
    db_url = os.getenv("DATABASE_URL")

    consumer_subscribe = ["canonical-clinical-events"]
    svc = PersistenceService(consumer_conf, consumer_subscribe, db_url)
    svc.start()