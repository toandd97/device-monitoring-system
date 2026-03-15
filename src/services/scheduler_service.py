import time
import random
from typing import List

from config.settings import settings
from src.common.logger import get_logger
from src.common.utils import utc_now_iso
from src.clients.metric_api import MetricAPI

logger = get_logger(__name__)

DEVICES: List[str] = ["router-01", "router-02", "db-server-01"]
METRICS: List[str] = ["cpu_usage", "ram_usage", "disk_usage"]

def _generate_metric_value(metric: str) -> float:
    if metric == "cpu_usage":
        return random.uniform(10, 95)
    if metric == "ram_usage":
        return random.uniform(20, 90)
    if metric == "disk_usage":
        return random.uniform(30, 99)
    return random.uniform(0, 100)

def build_fake_payload() -> dict:
    device_id = random.choice(DEVICES)
    metric = random.choice(METRICS)
    value = _generate_metric_value(metric)
    return {
        "device_id": device_id,
        "metric": metric,
        "value": round(value, 2),
        "timestamp": utc_now_iso(),
    }

def scheduler_loop() -> None:
    """Background loop that periodically sends fake metrics to the API."""
    time.sleep(3)  # small delay to ensure server is ready
    logger.info("Starting metric scheduler loop")

    # Assuming settings.api_base_url is an AnyUrl object, convert to string
    api_client = MetricAPI(base_url=str(settings.api_base_url))

    while True:
        payload = build_fake_payload()
        try:
            api_client.send_metric(payload)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Scheduler failed to send metric: %s", exc)

        time.sleep(settings.scheduler_interval_seconds)

