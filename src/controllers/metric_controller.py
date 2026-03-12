from fastapi import APIRouter, Depends

from src.common.response import success_response
from src.services.metric_service import MetricService
from src.validators.metric_validator import MetricRequest


router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


def get_metric_service() -> MetricService:
    return MetricService()


@router.post("")
async def create_metric(
    request: MetricRequest,
    service: MetricService = Depends(get_metric_service),
):
    result = service.process_metric(request)
    return success_response(data=result, message="Metric processed")

