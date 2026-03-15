from fastapi import APIRouter, Depends

from src.controllers.metric_controller import MetricController
from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest


router = APIRouter(tags=["Metrics V1"])


# ── Dependency Injection ──────────────────────────────────────────────────────

def get_service():
    start_time = time.time() # 1. Ghi lại giờ bắt đầu
    service = Service()
    try:
        yield service
    finally:
        process_time = time.time() - start_time # 2. Tính thời gian đã trôi qua
        print(f"Request handled in {process_time} seconds") # 3. Log lại


def get_metric_controller(
    service: MetricService = Depends(get_metric_service),
) -> MetricController:
    """Khởi tạo MetricController với service được inject."""
    return MetricController(metric_service=service)


# ── Routes ────────────────────────────────────────────────────────────────────
# Mỗi route chỉ có 1 nhiệm vụ: nhận HTTP request → chuyển cho controller xử lý.
# Không chứa bất kỳ business logic nào ở đây.

@router.post("", summary="Ghi nhận metric từ thiết bị")
async def create_metric(
    request: MetricRequest,
    controller: MetricController = Depends(get_metric_controller),
):
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

