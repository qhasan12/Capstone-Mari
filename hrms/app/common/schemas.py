from pydantic import BaseModel
from typing import Optional, Any


class APIResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None