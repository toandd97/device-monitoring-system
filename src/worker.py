import asyncio
from src.common.logger import get_logger
from src.services.consumer_service import run_consumer_loop
from config.settings import settings

logger = get_logger(__name__)

async def main():
    if not settings.consumer_enabled:
        logger.info("Consumer is disabled via settings. Exiting.")
        return
    logger.info("Starting Consumer Worker Service...")
    await run_consumer_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker Service stopped.")
