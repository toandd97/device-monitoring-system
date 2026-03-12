from typing import Dict, Any

from config.settings import settings


def get_kafka_producer_config() -> Dict[str, Any]:
    return {
        "bootstrap_servers": settings.kafka_bootstrap_servers,
        "client_id": "device-monitoring-producer",
        "acks": "all",
        "retries": 3,
    }


def get_kafka_consumer_config(group_id: str) -> Dict[str, Any]:
    return {
        "bootstrap_servers": settings.kafka_bootstrap_servers,
        "group_id": group_id,
        "auto_offset_reset": "earliest",
        "enable_auto_commit": False,
    }

