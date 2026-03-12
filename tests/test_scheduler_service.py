from src.services.scheduler_service import build_fake_payload


def test_build_fake_payload_structure():
    payload = build_fake_payload()

    assert "device_id" in payload
    assert "metric" in payload
    assert "value" in payload
    assert "timestamp" in payload

    assert isinstance(payload["device_id"], str)
    assert isinstance(payload["metric"], str)
    assert isinstance(payload["value"], float) or isinstance(
        payload["value"], int
    )
