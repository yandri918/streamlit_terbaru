from typing import Any, List, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

    @classmethod
    def ok(cls, data: Any = None, message: str = "OK") -> "ApiResponse":
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str, errors: List[str] = None) -> "ApiResponse":
        return cls(success=False, message=message, errors=errors or [])
