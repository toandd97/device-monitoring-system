import asyncio
from typing import Dict, Any

from src.common.logger import get_logger
from src.kafka.consumer import KafkaEventConsumer
from src.services.alert_service import get_alert_service

logger = get_logger(__name__)

def process_event(event: Dict[str, Any]) -> None:
    """Callback for processing Kafka events."""
    logger.debug("Received event: %s", event)
    
    payload = event.get("payload", {})
    device_id = payload.get("device_id", "unknown")
    metric = payload.get("metric", "unknown")
    value = payload.get("value", 0)
    
    # Simple logic: If we receive the alert, we check if it's critical.
    # Note: In a real microservice, the ingestion service might just dump to Kafka,
    # and this consumer performs the actual "Analysis".
    
    # Requirement 4 & 6: Analyze against thresholds and trigger alerts.
    # The MetricService already evaluates status and puts it in MongoDB, 
    # but the Event format in AI_INSTRUCTIONS.md doesn't include "status" in payload.
    # I'll re-evaluate it here or assume the ingestion service might include it in the future.
    # For now, I'll re-evaluate based on a standard threshold or check if status is present.
    
    status = event.get("status") # If ingestion service included it
    if not status:
        # Re-evaluate or just alert if value is high (simple dummy logic for this test)
        if value >= 80: # Critical threshold from description.md
            status = "CRITICAL"

    if status == "CRITICAL":
        alert_msg = f"Device: {device_id}\nMetric: {metric}\nValue: {value}\nStatus: {status}"
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
