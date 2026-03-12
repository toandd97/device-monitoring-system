from typing import Literal

from src.common.utils import generate_uuid, utc_now_iso
from src.database.base_model import BaseModel


MetricStatus = Literal["NORMAL", "WARNING", "CRITICAL"]


class MetricDocument(BaseModel):
    collection_name = "metrics"

    @staticmethod
    def build_document(
        device_id: str,
        metric: str,
        value: float,
        status: MetricStatus,
        timestamp: str,
    ) -> dict:
        return {
            "_id": generate_uuid(),
            "device_id": device_id,
            "metric": metric,
            "value": value,
            "status": status,
            "timestamp": timestamp or utc_now_iso(),
        }

