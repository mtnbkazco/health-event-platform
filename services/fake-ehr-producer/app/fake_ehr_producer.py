import os
import time
import uuid
from functools import partial

from confluent_kafka import Producer
from app.resource_generator import ResourceGenerator
from services.config.logger_config import get_logger, trace_id


class FakeEHRProducer:
    def __init__(self, conf, topic):
        self.logger = get_logger("fake-ehr-producer")
        self.producer = Producer(conf)
        self.topic = topic

    def delivery_report(self, error, message, event_id, tenant, trace_id):
        if error is not None:
            self.logger.error(f"Delivery failed: {error}")
        else:
            self.logger.info(
                f"Delivered to {message.topic()} [{message.partition()}]",
                extra={
                    "event_id": event_id,
                    "tenant": tenant,
                    "trace_id": trace_id.get()
                }
            )

    def start(self):
        self.logger.info("FakeEhrProducer service started...")
        while True:
            trace_uuid = str(uuid.uuid4())
            trace_id.set(trace_uuid)
            event = ResourceGenerator()
            event_json = event.generate_payload()
            event_id = str(uuid.uuid4())

            # metadata for callback
            callback_with_data = partial(
                self.delivery_report,
                event_id=event_id,
                tenant=event.tenant,
                trace_id=trace_id
            )

            self.producer.produce(
                topic,
                key=f"{event.tenant}:{event.patient_id}",
                value=event_json,
                headers=[("trace_id", trace_id.get().encode('utf-8'))],
                callback=callback_with_data
            )
            self.producer.poll(0)
            time.sleep(8)


if __name__ == "__main__":
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    topic = 'raw-clinical-events'
    conf = {'bootstrap.servers': kafka_server}
    svc = FakeEHRProducer(conf, topic)
    svc.start()



