import yaml
import logging
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("topic-create")

def migrate_topics(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    admin_client = AdminClient({
        'bootstrap.servers': 'localhost:9092'
    })
    # fetch existing topics to avoid 'topic already exists'
    kafka_metadata = admin_client.list_topics(timeout=10)
    existing_topics = kafka_metadata.topics.keys()

    new_topics = []
    for topic in config['topics']:
        if topic['name'] not in existing_topics:
            new_topics.append(
                NewTopic(
                    topic=topic['name'],
                    num_partitions=topic['partitions'],
                    replication_factor=topic['replication_factor'],
                    config=topic.get('config', {})
                )
            )
            logger.info(f"Preparing to create topic: {topic['name']}")

    if new_topics:
        fs = admin_client.create_topics(new_topics)
        for topic, file in fs.items():
            try:
                file.result()
                logger.info(f"Successfully created topic: {topic}")
            except Exception as e:
                logger.error(f"Failed to create {topic}-topic: {e}")
    else:
        logger.info("All topics already exist. No changes needed.")

if __name__ == "__main__":
    migrate_topics("topics.yaml")