from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    joining_date: Optional[date] = None


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    joining_date: Optional[date] = None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    department_id: Optional[int]
    role_id: Optional[int]
    joining_date: Optional[date]