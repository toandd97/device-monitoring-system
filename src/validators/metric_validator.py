from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, validator


class MetricRequest(BaseModel):
    device_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="ID of the device (cannot be empty)"
    )
    metric: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Name of the metric (e.g., cpu_usage, ram_usage)"
    )
    value: float = Field(
        ..., 
        ge=0.0, 
        description="Value of the metric. Must be greater than or equal to 0"
    )
    timestamp: str = Field(
        ...,
        description="Timestamp in ISO8601 format (e.g., '2025-12-10T10:00:00Z')"
    )

    @validator("timestamp")
    def validate_timestamp(cls, v: str) -> str:  # noqa: N805
        if not v or not v.strip():
            raise ValueError("timestamp cannot be empty")
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be in valid ISO8601 format")
        return v


MetricLevel = Literal["normal", "warning", "critical"]


class ThresholdConfig(BaseModel):
    normal: float = 60.0
    warning: float = 61.0
    critical: float = 80.0

