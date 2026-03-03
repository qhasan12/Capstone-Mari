from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RoleBase(BaseModel):
    title: str
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleResponse(BaseModel):
    id: int
    title: str
    level: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True