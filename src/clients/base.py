import httpx
from typing import Any, Dict, Optional
from src.common.logger import get_logger

logger = get_logger(__name__)

class BaseAPI:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        url = self._get_url(endpoint)
        try:
            response = httpx.post(url, json=data, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while calling {url}: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        url = self._get_url(endpoint)
        try:
            response = httpx.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Error calling {url}: {e}")
            raise
