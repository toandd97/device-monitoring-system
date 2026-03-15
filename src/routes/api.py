from fastapi import APIRouter
from src.routes.v1.metric_router import router as metric_router_v1

router = APIRouter(prefix="/api")

# Đăng ký các route của phiên bản V1
router.include_router(metric_router_v1, prefix="/v1/metrics")

# Để mở rộng sau này cho V2:
# from src.routes.v2.metric_router import router as metric_router_v2
# router.include_router(metric_router_v2, prefix="/v2/metrics")
