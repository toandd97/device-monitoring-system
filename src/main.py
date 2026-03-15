import uvicorn
from fastapi import FastAPI

from config.settings import settings
from src.common.logger import get_logger
from src.routes.api import router as main_api_router


logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Device Monitoring System")

    app.include_router(main_api_router)

    @app.on_event("startup")
    async def _on_startup() -> None:  # noqa: D401
        """Run startup tasks if any."""
        logger.info("Starting API Service...")

    @app.on_event("shutdown")
    def _on_shutdown() -> None:
        """Ngắt kết nối MongoDB khi tắt hệ thống."""
        from src.database.mongo_connection import MongoConnection
        MongoConnection.close()
        logger.info("Application shutdown: MongoDB connection closed.")

    return app


app = create_app()


if __name__ == "__main__":
    logger.info("Starting API on port %s", settings.api_port)
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.api_port, reload=False)

