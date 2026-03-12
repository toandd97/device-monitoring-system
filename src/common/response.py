from typing import Any, Dict, Optional

from fastapi import status
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    http_status: int = status.HTTP_200_OK,
) -> JSONResponse:
    body: Dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=http_status, content=body)


def error_response(
    message: str = "Error",
    http_status: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Any] = None,
) -> JSONResponse:
    body: Dict[str, Any] = {
        "success": False,
        "message": message,
    }
    if details is not None:
        body["details"] = details
    return JSONResponse(status_code=http_status, content=body)

