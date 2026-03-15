from src.services.consumer_service import process_event

class MockAlertService:
    def __init__(self):
        self.alerts = []
    def send_alert(self, message):
        self.alerts.append(message)
        return True

def test_process_event_triggers_alert_on_critical(monkeypatch):
    mock_alert_svc = MockAlertService()
    monkeypatch.setattr("src.services.consumer_service.get_alert_service", lambda: mock_alert_svc)
    
    # Event with status CRITICAL
    event = {
        "status": "CRITICAL",
        "payload": {
            "device_id": "test-device",
            "metric": "cpu_usage",
            "value": 95
        }
    }
    
    process_event(event)
    
    assert len(mock_alert_svc.alerts) == 1
    assert "test-device" in mock_alert_svc.alerts[0]
    assert "95" in mock_alert_svc.alerts[0]

def test_process_event_skips_on_normal(monkeypatch):
    mock_alert_svc = MockAlertService()
    monkeypatch.setattr("src.services.consumer_service.get_alert_service", lambda: mock_alert_svc)
    
    event = {
        "status": "NORMAL",
        "payload": {
            "device_id": "test-device",
            "metric": "cpu_usage",
            "value": 30
        }
    }
    
    process_event(event)
    assert len(mock_alert_svc.alerts) == 0

def test_process_event_evaluates_if_status_missing(monkeypatch):
    mock_alert_svc = MockAlertService()
    monkeypatch.setattr("src.services.consumer_service.get_alert_service", lambda: mock_alert_svc)
    
    # Missing status but value is high
    event = {
        "payload": {
            "device_id": "test-device",
            "metric": "cpu_usage",
            "value": 85
        }
    }
    
    process_event(event)
    assert len(mock_alert_svc.alerts) == 1
