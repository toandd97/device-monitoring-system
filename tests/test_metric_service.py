from types import SimpleNamespace

from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest, ThresholdConfig


class FakeProducer:
    def __init__(self) -> None:
        self.published = []

    def publish_event(self, event) -> None:  # noqa: D401
        """Record events instead of sending to Kafka."""
        self.published.append(event)


class FakeMetricDocument:
    inserted = []

    @classmethod
    def insert_one(cls, document):
        cls.inserted.append(document)
        return document.get("_id", "fake-id")

    @staticmethod
    def build_document(**kwargs):
        kwargs.setdefault("_id", "fake-id")
        return kwargs


def test_evaluate_status_levels(monkeypatch):
    fake_producer = FakeProducer()
    monkeypatch.setattr("src.services.metric_service.KafkaEventProducer", lambda: fake_producer)
    
    svc = MetricService(ThresholdConfig(normal=60, warning=70, critical=80))

    assert svc._evaluate_status(50) == "NORMAL"  # noqa: SLF001
    assert svc._evaluate_status(75) == "WARNING"  # noqa: SLF001
    assert svc._evaluate_status(85) == "CRITICAL"  # noqa: SLF001


def test_process_metric_persists_and_publishes(monkeypatch):
    fake_producer = FakeProducer()
    monkeypatch.setattr("src.services.metric_service.KafkaEventProducer", lambda: fake_producer)
    monkeypatch.setattr("src.services.metric_service.MetricDocument", FakeMetricDocument)

    svc = MetricService()

    req = MetricRequest(
        device_id="router-01",
        metric="cpu_usage",
        value=92,
        timestamp="2025-12-10T10:00:00Z",
    )

    result = svc.process_metric(req)

    assert result["status"] == "CRITICAL"
    assert FakeMetricDocument.inserted, "Document should be inserted to Mongo"
    assert fake_producer.published, "Event should be published to Kafka"

