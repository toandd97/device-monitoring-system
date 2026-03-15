import asyncio
from typing import Dict, Any

from src.common.logger import get_logger
from src.kafka.consumer import KafkaEventConsumer
from src.services.alert_service import get_alert_service
from src.validators.metric_validator import ThresholdConfig
from src.models.metric_model import MetricDocument, MetricFields, MetricStatus

logger = get_logger(__name__)

def _evaluate_status(value: float, thresholds: ThresholdConfig) -> str:
    if value >= thresholds.critical:
        return MetricStatus.CRITICAL
    if value >= thresholds.warning:
        return MetricStatus.WARNING
    return MetricStatus.NORMAL

def process_event(event: Dict[str, Any]) -> None:
    """Callback for processing Kafka events."""
    logger.debug("Received event: %s", event)
    
    if not event:
        logger.warning("Received empty or None event")
        return
        
    payload = event.get(MetricFields.PAYLOAD) or {}
    device_id = payload.get("device_id", "unknown")
    metric = payload.get("metric", "unknown")
    value = payload.get("value", 0)
    timestamp = event.get(MetricFields.TIMESTAMP)
    
    # Analyze against thresholds
    thresholds = ThresholdConfig()
    status = _evaluate_status(float(value), thresholds)

    # Store results in MongoDB
    try:
        document = MetricDocument.build_document(event, status)
        MetricDocument.insert_one(document)
        logger.info(f"Stored metric event {document.get(MetricFields.EVENT_ID)} for {device_id} with status {status}")
    except Exception as e:
        logger.error(f"Failed to store metric event in MongoDB: {e}")

    # Trigger alerts when values are critical
    if status == MetricStatus.CRITICAL:
        alert_msg = (
            f"<b>Device:</b> {device_id}\n"
            f"<b>Metric:</b> {metric}\n"
            f"<b>Value:</b> {value}\n"
            f"<b>Status:</b> {status}"
        )
        get_alert_service().send_alert(alert_msg)

async def run_consumer_loop() -> None:
    """Run the Kafka consumer in a background thread or asyncio-friendly way."""
    logger.info("Initializing Kafka Consumer Service")
    
    # Since kafka-python consumer is blocking, we run it in a thread
    def start_sync_consumer():
        consumer = KafkaEventConsumer(group_id="analysis-group", on_event=process_event)
        try:
            consumer.consume()
        finally:
            consumer.close()

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, start_sync_consumer)
