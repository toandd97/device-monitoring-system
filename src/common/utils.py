import uuid
from datetime import datetime, timezone
from typing import Any, Dict


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_event(
    source: str,
    payload: Dict[str, Any],
    event_type: str = "metric.reported",
) -> Dict[str, Any]:
    from src.models.metric_model import MetricFields
    return {
        MetricFields.EVENT_ID: generate_uuid(),
        MetricFields.EVENT_TYPE: event_type,
        MetricFields.TIMESTAMP: utc_now_iso(),
        MetricFields.SOURCE: source,
        MetricFields.PAYLOAD: payload,
    }

