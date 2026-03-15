import pytest
from src.services.alert_service import AlertService

class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")
    def json(self):
        return {"ok": True}

def test_alert_service_skips_when_not_configured(monkeypatch):
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_token", None)
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_chat_id", None)
    
    svc = AlertService()
    assert svc.send_alert("test") is False

def test_alert_service_sends_successfully(monkeypatch):
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_token", "fake_token")
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_chat_id", "fake_id")
    
    def mock_post(*args, **kwargs):
        return MockResponse(200)
    
    monkeypatch.setattr("httpx.post", mock_post)
    
    svc = AlertService()
    assert svc.send_alert("test message") is True

def test_alert_service_handles_error(monkeypatch):
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_token", "fake_token")
    monkeypatch.setattr("src.services.alert_service.settings.alert_telegram_chat_id", "fake_id")
    
    def mock_post(*args, **kwargs):
        return MockResponse(500)
    
    monkeypatch.setattr("httpx.post", mock_post)
    
    svc = AlertService()
    assert svc.send_alert("test message") is False
