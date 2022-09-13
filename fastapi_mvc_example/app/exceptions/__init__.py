"""Application implementation - exceptions."""
from fastapi_mvc_example.app.exceptions.http import (
    HTTPException,
    http_exception_handler,
)


__all__ = ("HTTPException", "http_exception_handler")
