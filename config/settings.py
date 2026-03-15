import os
from functools import lru_cache
from pydantic import BaseSettings, Field, AnyUrl


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    api_port: int = Field(8000, alias="API_PORT")

    # Scheduler / simulator
    scheduler_enabled: bool = Field(True, alias="SCHEDULER_ENABLED")
    scheduler_interval_seconds: int = Field(5, alias="SCHEDULER_INTERVAL_SECONDS")
    api_base_url: AnyUrl = Field("http://localhost:8000", alias="API_BASE_URL")

    kafka_bootstrap_servers: str = Field("kafka:9092", alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic_metrics: str = Field("device.metrics.raw", alias="KAFKA_TOPIC_METRICS")

    mongo_uri: AnyUrl = Field("mongodb://mongo:27017", alias="MONGO_URI")
    mongo_db_name: str = Field("device_monitoring", alias="MONGO_DB_NAME")

    # Consumer / alerting
    consumer_enabled: bool = Field(True, alias="CONSUMER_ENABLED")
    alert_telegram_token: str | None = Field(None, alias="ALERT_TELEGRAM_TOKEN")
    alert_telegram_chat_id: str | None = Field(None, alias="ALERT_TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

