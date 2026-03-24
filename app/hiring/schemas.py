from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# =====================================================
# Hiring Request Schemas
# =====================================================

class HiringRequestBase(BaseModel):
    department_id: int
    role_title: str
    manager_id: int
    required_skills: str
    experience_level: str
    budget_range: str
    status: Optional[str] = Field(default="Draft")
    jd_text: Optional[str] = None
    is_active: Optional[bool] = True  # Add this for soft delete support


class HiringRequestCreate(HiringRequestBase):
    pass


class HiringRequestUpdate(BaseModel):
    department_id: Optional[int] = None
    role_title: Optional[str] = None
    required_skills: Optional[str] = None
    manager_approved:Optional[bool] =None
    experience_level: Optional[str] = None
    budget_range: Optional[str] = None
    status: Optional[str] = None
    jd_text: Optional[str] = None
    is_active: Optional[bool] = None  # Allow soft delete updates


class HiringRequestResponse(HiringRequestBase):
    id: int
    manager_id: Optional[int] = None
    manager_approved: bool
    manager_approved_at: Optional[datetime]
    created_by: Optional[int]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# =====================================================
# Job Posting Schemas
# =====================================================

class JobPostingBase(BaseModel):
    hiring_request_id: int
    posted_date: Optional[date] = None
    closing_date: Optional[date] = None
    status: Optional[str] = Field(default="Draft")
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