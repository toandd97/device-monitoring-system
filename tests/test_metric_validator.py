import pytest
from fastapi import HTTPException

from src.validators.metric_validator import MetricRequest, validate_create_metric


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


def test_missing_device_id_raises():
    req = MetricRequest(metric="cpu_usage", value=50.5, timestamp="2025-12-10T10:00:00Z")
    with pytest.raises(HTTPException) as exc_info:
        validate_create_metric(req)
    assert exc_info.value.status_code == 422
    fields = [e["field"] for e in exc_info.value.detail]
    assert "device_id" in fields


def test_missing_metric_raises():
    req = MetricRequest(device_id="router-01", value=50.5, timestamp="2025-12-10T10:00:00Z")
    with pytest.raises(HTTPException) as exc_info:
        validate_create_metric(req)
    assert exc_info.value.status_code == 422
    fields = [e["field"] for e in exc_info.value.detail]
    assert "metric" in fields


def test_missing_value_raises():
    req = MetricRequest(device_id="router-01", metric="cpu_usage", timestamp="2025-12-10T10:00:00Z")
    with pytest.raises(HTTPException) as exc_info:
        validate_create_metric(req)
    assert exc_info.value.status_code == 422
    fields = [e["field"] for e in exc_info.value.detail]
    assert "value" in fields


def test_invalid_timestamp_raises():
    req = MetricRequest(
        device_id="router-01",
        metric="cpu_usage",
        value=50.5,
        timestamp="invalid-timestamp",
    )
    with pytest.raises(HTTPException) as exc_info:
        validate_create_metric(req)
    assert exc_info.value.status_code == 422
    fields = [e["field"] for e in exc_info.value.detail]
    assert "timestamp" in fields


def test_negative_value_raises():
    req = MetricRequest(
        device_id="router-01",
        metric="cpu_usage",
        value=-1.0,
        timestamp="2025-12-10T10:00:00Z",
    )
    with pytest.raises(HTTPException) as exc_info:
        validate_create_metric(req)
    assert exc_info.value.status_code == 422
    fields = [e["field"] for e in exc_info.value.detail]
    assert "value" in fields


def test_valid_all_fields_no_error():
    req = MetricRequest(
        device_id="router-01",
        metric="cpu_usage",
        value=92.0,
        timestamp="2025-12-10T10:00:00Z",
    )
    # Should not raise
    validate_create_metric(req)
