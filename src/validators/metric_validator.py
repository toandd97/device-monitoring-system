from datetime import datetime
from typing import Literal, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel


class MetricRequest(BaseModel):
    device_id: Optional[str] = None
    metric: Optional[str] = None
    value: Optional[float] = None
    timestamp: Optional[str] = None


def validate_create_metric(request: MetricRequest) -> None:
    """Validate business rules for creating a metric.
    Raises HTTP 422 with a descriptive message for each invalid field.
    """
    errors = []

    # device_id: required, must be a non-empty string
    if request.device_id is None:
        errors.append({"field": "device_id", "message": "device_id is required"})
    elif not isinstance(request.device_id, str) or not request.device_id.strip():
        errors.append({"field": "device_id", "message": "device_id must be a non-empty string"})

    # metric: required, must be a non-empty string
    if request.metric is None:
        errors.append({"field": "metric", "message": "metric is required"})
    elif not isinstance(request.metric, str) or not request.metric.strip():
        errors.append({"field": "metric", "message": "metric must be a non-empty string"})

    # value: required, must be int or float (not string, not bool), must be >= 0
    if request.value is None:
        errors.append({"field": "value", "message": "value is required"})
    elif isinstance(request.value, bool):
        errors.append({"field": "value", "message": "value must be a number (int or float), not a boolean"})
    elif not isinstance(request.value, (int, float)):
        errors.append({"field": "value", "message": "value must be a valid number (int or float)"})
    elif request.value < 0:
        errors.append({"field": "value", "message": "value must be >= 0"})

    # timestamp: required, must be valid ISO8601 string
    if request.timestamp is None:
        errors.append({"field": "timestamp", "message": "timestamp is required"})
    elif not isinstance(request.timestamp, str) or not request.timestamp.strip():
        errors.append({"field": "timestamp", "message": "timestamp must be a non-empty string"})
    else:
        try:
            datetime.fromisoformat(request.timestamp.replace("Z", "+00:00"))
        except ValueError:
            errors.append({"field": "timestamp", "message": "timestamp must be a valid ISO8601 format (e.g., '2025-12-10T10:00:00Z')"})

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
        )


MetricLevel = Literal["normal", "warning", "critical"]


class ThresholdConfig(BaseModel):
    normal: float = 60.0
    warning: float = 61.0
    critical: float = 80.0
