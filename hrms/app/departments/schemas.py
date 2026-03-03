from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DepartmentCreate(BaseModel):
    name: str
    is_active: Optional[bool] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True