import httpx
from typing import Any, Dict
from src.clients.base import BaseAPI
from src.common.logger import get_logger

logger = get_logger(__name__)

class MetricAPI(BaseAPI):
    def __init__(self, base_url: str, timeout: float = 10.0):
        super().__init__(base_url=base_url, timeout=timeout)
        self.metrics_endpoint = "/api/v1/metrics"

    def send_metric(self, payload: Dict[str, Any]) -> httpx.Response:
        """
        Sends a metric payload to the API.
        """
        logger.info(f"Sending metric to {self._get_url(self.metrics_endpoint)}: {payload}")
        return self.post(endpoint=self.metrics_endpoint, data=payload)
