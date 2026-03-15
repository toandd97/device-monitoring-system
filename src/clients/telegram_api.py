from typing import Any, Dict, Optional
from src.clients.base import BaseAPI
from src.clients.endpoints import TELEGRAM_SEND_MESSAGE
from src.common.logger import get_logger

logger = get_logger(__name__)

class TelegramAPI(BaseAPI):
    def __init__(self, token: str):
        base_url = f"https://api.telegram.org/bot{token}"
        super().__init__(base_url)

    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        response = self.post(TELEGRAM_SEND_MESSAGE, data=payload)
        return response.json()
