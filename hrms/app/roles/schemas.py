from pydantic import BaseModel
<<<<<<< HEAD
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
=======
from datetime import datetime
from typing import Optional


class RoleBase(BaseModel):
    title: str
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleCreate(RoleBase):
    pass

>>>>>>> dev-branch

class RoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None
<<<<<<< HEAD


# ==============================
# RESPONSE
# ==============================

=======
    is_active: Optional[bool] = None


>>>>>>> dev-branch
class RoleResponse(BaseModel):
    id: int
    title: str
    level: Optional[int]
    description: Optional[str]
<<<<<<< HEAD
=======
    is_active: bool
    created_at: datetime
    updated_at: datetime
>>>>>>> dev-branch

    class Config:
        from_attributes = True