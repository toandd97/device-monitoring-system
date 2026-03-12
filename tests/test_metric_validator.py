import pytest

from src.validators.metric_validator import MetricRequest


def test_valid_metric_request():
    req = MetricRequest(
        device_id="router-01",
        metric="cpu_usage",
        value=50.5,
        timestamp="2025-12-10T10:00:00Z",
    )

    assert req.device_id == "router-01"
    assert req.metric == "cpu_usage"
    assert req.value == 50.5


def test_invalid_timestamp_raises():
    with pytest.raises(ValueError):
        MetricRequest(
            device_id="router-01",
            metric="cpu_usage",
            value=50.5,
            timestamp="invalid-timestamp",
        )

