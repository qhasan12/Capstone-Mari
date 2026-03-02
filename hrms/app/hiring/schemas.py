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


class HiringRequestResponse(HiringRequestBase):
    id: int
    # Include timestamps if added in model
    # created_at: datetime
    # updated_at: datetime

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


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(BaseModel):
    posted_date: Optional[date] = None
    closing_date: Optional[date] = None
    status: Optional[str] = None


class JobPostingResponse(JobPostingBase):
    id: int

    class Config:
        from_attributes = True