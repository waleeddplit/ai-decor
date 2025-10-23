"""
Common Pydantic models used across the application
"""

from typing import Optional, Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response"""

    error: str
    detail: Optional[str] = None
    status_code: int = 400


class SuccessResponse(BaseModel):
    """Standard success response"""

    message: str
    data: Optional[Any] = None
    status_code: int = 200

