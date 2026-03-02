from pydantic import BaseModel
from datetime import date
from typing import Optional


# ==============================
# LEAVE TYPE
# ==============================

class LeaveTypeCreate(BaseModel):
    name: str
    default_allocation: int


class LeaveTypeResponse(BaseModel):
    id: int
    name: str
    default_allocation: int

    class Config:
        from_attributes = True


# ==============================
# LEAVE BALANCE
# ==============================

class LeaveBalanceCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    total_leaves: int


class LeaveBalanceResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    total_leaves: int
    used_leaves: int
    remaining_leaves: int

    class Config:
        from_attributes = True


# ==============================
# LEAVE REQUEST
# ==============================

class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveRequestUpdate(BaseModel):
    status: str


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str]
    status: str

    class Config:
        from_attributes = True