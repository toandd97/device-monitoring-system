from typing import Any, Dict

from kafka import KafkaProducer
import json

from config.kafka_config import get_kafka_producer_config
from config.settings import settings
from src.common.logger import get_logger


logger = get_logger(__name__)


class KafkaEventProducer:
    def __init__(self) -> None:
        cfg = get_kafka_producer_config()
        self._producer = KafkaProducer(
            **cfg,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish_event(self, event: Dict[str, Any]) -> None:
        topic = settings.kafka_topic_metrics
        logger.info("Publishing event to topic %s", topic)
        self._producer.send(topic, value=event)
        self._producer.flush()

    def close(self) -> None:
        logger.info("Closing Kafka producer")
        self._producer.close()

