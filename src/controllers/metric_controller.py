from src.common.response import success_response
from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest


class MetricController:
    def __init__(self, metric_service: MetricService):
        self.metric_service = metric_service

    def create_metric(self, request: MetricRequest):
        result = self.metric_service.process_metric(request)
        return success_response(data=result, message="Metric processed")

    # def get_all_metrics(self):
    #     result = self.metric_service.get_all_metrics()
    #     return success_response(data=result, message="Metrics retrieved")

    # def get_metrics_by_device(self, device_id: str):
    #     result = self.metric_service.get_metrics_by_device(device_id)
    #     return success_response(data=result, message=f"Metrics for device '{device_id}' retrieved")


