from fastapi import APIRouter, Depends

from src.controllers.metric_controller import MetricController
from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest, validate_create_metric


router = APIRouter(tags=["Metrics V1"])


def get_metric_service() -> MetricService:
    return MetricService()


def get_metric_controller(
    service: MetricService = Depends(get_metric_service),
) -> MetricController:
    return MetricController(metric_service=service)


@router.post("", summary="Ghi nhận metric từ thiết bị")
def create_metric(
    request: MetricRequest,
    controller: MetricController = Depends(get_metric_controller),
):
    validate_create_metric(request)
    return controller.create_metric(request)


@router.get("", summary="Lấy toàn bộ danh sách metrics")
async def get_all_metrics(
    controller: MetricController = Depends(get_metric_controller),
):
    return controller.get_all_metrics()


@router.get("/{device_id}", summary="Lấy metrics theo device_id")
async def get_metrics_by_device(
    device_id: str,
    controller: MetricController = Depends(get_metric_controller),
):
    return controller.get_metrics_by_device(device_id)

