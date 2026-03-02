from pydantic import BaseModel
from typing import Optional


# -----------------------
# Base
# -----------------------

class RoleBase(BaseModel):
    title: str
    level: Optional[int] = None
    description: Optional[str] = None


# -----------------------
# Create
# -----------------------

class RoleCreate(RoleBase):
    pass


# -----------------------
# Update
# -----------------------

class RoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None


# -----------------------
# Response
# -----------------------

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True