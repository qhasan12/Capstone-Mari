from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    personal_email: EmailStr
    department_id: int
    role_id: int
    manager_id: Optional[int] = None
    joining_date: Optional[date] = None
    salary: Optional[float] = None
    # created_by: int
    # created_at: datetime


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    personal_email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    manager_id: Optional[int] = None
    joining_date: Optional[date] = None
    salary: Optional[float] = None
    is_active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    personal_email: EmailStr
    department_id: int
    role_id: int
    manager_id: Optional[int]
    joining_date: Optional[date]
    salary: Optional[float]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True