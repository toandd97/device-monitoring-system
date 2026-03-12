import asyncio

import uvicorn
from fastapi import FastAPI

from config.settings import settings
from src.common.logger import get_logger
from src.controllers.metric_controller import router as metric_router
from src.services.scheduler_service import scheduler_loop


logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Device Monitoring System")

    app.include_router(metric_router)

    @app.on_event("startup")
    async def _start_scheduler() -> None:  # noqa: D401
        """Start background scheduler to simulate metrics."""
        if settings.scheduler_enabled:
            logger.info("Scheduler enabled, starting background task")
            asyncio.create_task(scheduler_loop())
        else:
            logger.info("Scheduler disabled via settings")

    return app


app = create_app()


if __name__ == "__main__":
    logger.info("Starting API on port %s", settings.api_port)
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.api_port, reload=False)

