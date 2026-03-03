from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Used for creating department
class DepartmentCreate(BaseModel):
    name: str


# Used for updating department
class DepartmentUpdate(BaseModel):
    name: Optional[str] = None


# Response model
class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # important for SQLAlchemy