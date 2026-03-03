from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# -----------------------
# Hiring Request Schemas
# -----------------------

class HiringRequestBase(BaseModel):
    department_id: int
    role_title: str
    required_skills: str
    experience_level: str
    budget_range: str
    status: Optional[str] = "Draft"
    jd_text: Optional[str] = None
    approval_status: Optional[str] = "Pending"


class HiringRequestCreate(HiringRequestBase):
    pass


class HiringRequestResponse(HiringRequestBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------
# Job Posting Schemas
# -----------------------

class JobPostingBase(BaseModel):
    hiring_request_id: int
    posted_date: date
    closing_date: date
    status: Optional[str] = "Open"


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingResponse(JobPostingBase):
    id: int

    class Config:
        from_attributes = True