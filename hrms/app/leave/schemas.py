from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional
from enum import Enum


class LeaveStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


# ==============================
# LEAVE TYPE
# ==============================

class LeaveTypeCreate(BaseModel):
    name: str
    default_allocation: int = Field(gt=0)


class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = None
    default_allocation: Optional[int] = Field(default=None, gt=0)
    is_active: Optional[bool] = None


class LeaveTypeResponse(BaseModel):
    id: int
    name: str
    default_allocation: int
    is_active: bool

    class Config:
        from_attributes = True


# ==============================
# LEAVE BALANCE
# ==============================

class LeaveBalanceCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    total_leaves: int = Field(gt=0)


class LeaveBalanceUpdate(BaseModel):
    total_leaves: Optional[int] = Field(default=None, gt=0)
    used_leaves: Optional[int] = None
    remaining_leaves: Optional[int] = None
    is_active: Optional[bool] = None


class LeaveBalanceResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    total_leaves: int
    used_leaves: int
    remaining_leaves: int
    is_active: bool

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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class LeaveRequestUpdate(BaseModel):
    status: Optional[LeaveStatus] = None
    is_active: Optional[bool] = None


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str]
    status: LeaveStatus
    is_active: bool

    class Config:
        from_attributes = True