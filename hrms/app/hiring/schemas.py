from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# =====================================================
# Hiring Request Schemas
# =====================================================

class HiringRequestBase(BaseModel):
    department_id: int
    role_title: str
    required_skills: str
    experience_level: str
    budget_range: str
    status: Optional[str] = Field(default="Draft")
    jd_text: Optional[str] = None
    approval_status: Optional[str] = Field(default="Pending")
    is_active: Optional[bool] = True  # Add this for soft delete support


class HiringRequestCreate(HiringRequestBase):
    pass


class HiringRequestUpdate(BaseModel):
    department_id: Optional[int] = None
    role_title: Optional[str] = None
    required_skills: Optional[str] = None
    experience_level: Optional[str] = None
    budget_range: Optional[str] = None
    status: Optional[str] = None
    jd_text: Optional[str] = None
    approval_status: Optional[str] = None
    is_active: Optional[bool] = None  # Allow soft delete updates


class HiringRequestResponse(HiringRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# =====================================================
# Job Posting Schemas
# =====================================================

class JobPostingBase(BaseModel):
    hiring_request_id: int
    posted_date: date
    closing_date: date
    status: Optional[str] = Field(default="Open")
    is_active: Optional[bool] = True  # For soft delete

class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(BaseModel):
    posted_date: Optional[date] = None
    closing_date: Optional[date] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None  # Allow soft delete updates


class JobPostingResponse(JobPostingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True