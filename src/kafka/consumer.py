from typing import Callable, Dict, Any

from kafka import KafkaConsumer
import json

from config.kafka_config import get_kafka_consumer_config
from config.settings import settings
from src.common.logger import get_logger


logger = get_logger(__name__)


class KafkaEventConsumer:
    def __init__(self, group_id: str, on_event: Callable[[Dict[str, Any]], None]) -> None:
        self._on_event = on_event
        cfg = get_kafka_consumer_config(group_id=group_id)
        self._consumer = KafkaConsumer(
            settings.kafka_topic_metrics,
            **cfg,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

    def consume(self) -> None:
        logger.info("Starting Kafka consumer loop")
        for message in self._consumer:
            event = message.value
            try:
                self._on_event(event)
                self._consumer.commit()
            except Exception as exc:  # noqa: BLE001
                logger.exception("Error processing event: %s", exc)

    def close(self) -> None:
        logger.info("Closing Kafka consumer")
        self._consumer.close()

