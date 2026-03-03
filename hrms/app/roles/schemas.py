from pydantic import BaseModel
from typing import Optional


# ==============================
# CREATE
# ==============================

class RoleCreate(BaseModel):
    title: str
    level: Optional[int] = None
    description: Optional[str] = None


# ==============================
# UPDATE
# ==============================

class RoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None


# ==============================
# RESPONSE
# ==============================

class RoleResponse(BaseModel):
    id: int
    title: str
    level: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True