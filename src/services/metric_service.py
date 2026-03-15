from typing import Dict, Any, List

from src.common.logger import get_logger
from src.common.utils import build_event
from src.kafka.producer import KafkaEventProducer
from src.models.metric_model import MetricDocument, MetricFields
from src.validators.metric_validator import ThresholdConfig, MetricRequest


logger = get_logger(__name__)


def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Chuyển _id ObjectId của MongoDB sang string để serialize JSON."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


class MetricService:
    def __init__(self, thresholds: ThresholdConfig | None = None) -> None:
        self.thresholds = thresholds or ThresholdConfig()
        self._producer = KafkaEventProducer()

    def process_metric(self, metric_req: MetricRequest) -> Dict[str, Any]:
        event_payload = {
            "device_id": metric_req.device_id,
            "metric": metric_req.metric,
            "value": metric_req.value,
        }
        event = build_event(source="ingestion-service", payload=event_payload)
        
        if event is not None:
            event[MetricFields.TIMESTAMP] = metric_req.timestamp
        
        self._producer.publish_event(event)

        logger.info(
            "Published metric event to Kafka for device %s",
            metric_req.device_id,
        )

        return {
            "event_id": event.get(MetricFields.EVENT_ID) if event else None,
            "status": "published_to_kafka",
        }

    def get_all_metrics(self) -> List[Dict[str, Any]]:
        raw = MetricDocument.find_all()
        return [_serialize(doc) for doc in raw]

    def get_metrics_by_device(self, device_id: str) -> List[Dict[str, Any]]:
        raw = MetricDocument.find_all(query={f"{MetricFields.PAYLOAD}.device_id": device_id})
        return [_serialize(doc) for doc in raw]

    def close(self) -> None:
        self._producer.close()

