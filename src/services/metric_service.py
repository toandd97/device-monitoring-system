from typing import Dict, Any

from src.common.logger import get_logger
from src.common.utils import build_event
from src.kafka.producer import KafkaEventProducer
from src.models.metric_model import MetricDocument, MetricStatus
from src.validators.metric_validator import ThresholdConfig, MetricRequest


logger = get_logger(__name__)


class MetricService:
    def __init__(self, thresholds: ThresholdConfig | None = None) -> None:
        self.thresholds = thresholds or ThresholdConfig()
        self._producer = KafkaEventProducer()

    def _evaluate_status(self, value: float) -> MetricStatus:
        if value >= self.thresholds.critical:
            return "CRITICAL"
        if value >= self.thresholds.warning:
            return "WARNING"
        return "NORMAL"

    def process_metric(self, metric_req: MetricRequest) -> Dict[str, Any]:
        status = self._evaluate_status(metric_req.value)

        # Persist to MongoDB
        document = MetricDocument.build_document(
            device_id=metric_req.device_id,
            metric=metric_req.metric,
            value=metric_req.value,
            status=status,
            timestamp=metric_req.timestamp,
        )
        MetricDocument.insert_one(document)

        # Publish event to Kafka
        event_payload = {
            "device_id": metric_req.device_id,
            "metric": metric_req.metric,
            "value": metric_req.value,
        }
        event = build_event(source="ingestion-service", payload=event_payload)
        self._producer.publish_event(event)

        logger.info(
            "Processed metric for device %s, status=%s",
            metric_req.device_id,
            status,
        )

        return {
            "status": status,
            "stored_document_id": document["_id"],
        }

    def close(self) -> None:
        self._producer.close()

