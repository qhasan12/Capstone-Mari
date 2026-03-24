from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==============================
# CREATE ONBOARDING
# ==============================

class OnboardingCreate(BaseModel):
    employee_id: int
    is_active: Optional[bool] = True


# ==============================
# UPDATE ONBOARDING
# ==============================

class OnboardingUpdate(BaseModel):
    appointment_letter_generated: Optional[bool] = None
    email_created: Optional[bool] = None
    resources_allocated: Optional[bool] = None
    orientation_sent: Optional[bool] = None
    # stage: Optional[str] = None
    is_active: Optional[bool] = True


# ==============================
# RESPONSE
# ==============================
class OnboardingResponse(BaseModel):
    id: int
    employee_id: int
    appointment_letter_generated: bool
    email_created: bool
    resources_allocated: bool
    orientation_sent: bool
    stage: Optional[str]
    is_active: Optional[bool] = True

    # ✅ ADD THESE
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None

    class Config:
        from_attributes = True