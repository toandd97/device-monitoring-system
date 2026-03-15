from src.common.response import success_response
from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest


class MetricController:
    """
    Controller xử lý các nghiệp vụ liên quan đến Metric.
    Hoàn toàn độc lập với framework HTTP — mọi service được inject qua __init__.
    """
    def __init__(self, metric_service: MetricService):
        self.metric_service = metric_service

    def create_metric(self, request: MetricRequest):
        """Nhận và xử lý một metric mới từ thiết bị."""
        result = self.metric_service.process_metric(request)
        return success_response(data=result, message="Metric processed")

    def get_all_metrics(self):
        """Trả về danh sách toàn bộ metrics đã ghi nhận."""
        result = self.metric_service.get_all_metrics()
        return success_response(data=result, message="Metrics retrieved")

    def get_metrics_by_device(self, device_id: str):
        """Trả về danh sách metrics theo device_id cụ thể."""
        result = self.metric_service.get_metrics_by_device(device_id)
        return success_response(data=result, message=f"Metrics for device '{device_id}' retrieved")


