import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.common.logger import get_logger

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware tự động ghi lại thời gian xử lý của mỗi HTTP request."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "%s %s → %d | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            process_time_ms,
        )
        return response
