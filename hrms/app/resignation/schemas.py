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
    is_active: Optional[bool] = True


class ResignationUpdate(BaseModel):
    manager_approved: Optional[bool] = None
    status: Optional[str] = None
    is_active: Optional[bool] = True

class ResignationResponse(BaseModel):
    id: int
    employee_id: int
    resignation_date: date
    notice_end_date: date
    manager_approved: bool
    status: Optional[str]
    is_active: Optional[bool] = True

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
    is_active: Optional[bool] = True

class ClearanceResponse(BaseModel):
    id: int
    resignation_id: int
    laptop_returned: Optional[bool] = False
    access_revoked: Optional[bool] = False
    email_deactivated: Optional[bool] = False
    clearance_completed: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True