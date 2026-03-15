from config.settings import settings
from src.common.logger import get_logger
from src.clients.telegram_api import TelegramAPI

logger = get_logger(__name__)

class AlertService:
    def __init__(self) -> None:
        self.token = settings.alert_telegram_token
        self.chat_id = settings.alert_telegram_chat_id
        self._api = None
        if self.token:
            self._api = TelegramAPI(self.token)

    def send_alert(self, message: str) -> bool:
        """Send alert to Telegram if configured."""
        logger.info("Triggering alert: %s", message)
        
        if not self._api or not self.chat_id:
            logger.warning("Telegram alerting is not fully configured. Skipping.")
            return False

        try:
            self._api.send_message(
                chat_id=self.chat_id,
                text=f"🚨 <b>DEVICE ALERT</b>\n\n{message}"
            )
            logger.info("Alert sent successfully to Telegram via API Layer")
            return True
        except Exception as exc:
            logger.error("Failed to send Telegram alert via API Layer: %s", exc)
            return False

_alert_service = AlertService()

def get_alert_service() -> AlertService:
    return _alert_service
