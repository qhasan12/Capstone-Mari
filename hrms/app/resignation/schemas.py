from pydantic import BaseModel
from datetime import date
from typing import Optional


# ==============================
# RESIGNATION
# ==============================

class ResignationCreate(BaseModel):
    employee_id: int
    resignation_date: date
    notice_end_date: date


class ResignationUpdate(BaseModel):
    manager_approved: Optional[bool] = None
    status: Optional[str] = None


class ResignationResponse(BaseModel):
    id: int
    employee_id: int
    resignation_date: date
    notice_end_date: date
    manager_approved: bool
    status: Optional[str]

    class Config:
        from_attributes = True


# ==============================
# CLEARANCE
# ==============================

class ClearanceUpdate(BaseModel):
    laptop_returned: Optional[bool] = None
    access_revoked: Optional[bool] = None
    email_deactivated: Optional[bool] = None
    clearance_completed: Optional[bool] = None


class ClearanceResponse(BaseModel):
    id: int
    resignation_id: int
    laptop_returned: bool
    access_revoked: bool
    email_deactivated: bool
    clearance_completed: bool

    class Config:
        from_attributes = True