from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, validator


class MetricRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    metric: str = Field(..., min_length=1)
    value: float
    timestamp: str

    @validator("timestamp")
    def validate_timestamp(cls, v: str) -> str:  # noqa: N805
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be in ISO8601 format")
        return v


MetricLevel = Literal["normal", "warning", "critical"]


class ThresholdConfig(BaseModel):
    normal: float = 60.0
    warning: float = 61.0
    critical: float = 80.0

