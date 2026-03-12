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
    return {
        "event_id": generate_uuid(),
        "event_type": event_type,
        "timestamp": utc_now_iso(),
        "source": source,
        "payload": payload,
    }

