from src.common.logger import get_logger
from src.services.scheduler_service import scheduler_loop
from config.settings import settings

logger = get_logger(__name__)

def main():
    if not settings.scheduler_enabled:
        logger.info("Scheduler is disabled via settings. Exiting.")
        return
    logger.info("Starting Simulator Service...")
    scheduler_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Simulator Service stopped.")
