from pydantic import BaseModel
from typing import Optional


# ==============================
# CREATE ONBOARDING
# ==============================

class OnboardingCreate(BaseModel):
    employee_id: int


# ==============================
# UPDATE ONBOARDING
# ==============================

class OnboardingUpdate(BaseModel):
    appointment_letter_generated: Optional[bool] = None
    email_created: Optional[bool] = None
    resources_allocated: Optional[bool] = None
    orientation_sent: Optional[bool] = None
    stage: Optional[str] = None


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

    class Config:
        from_attributes = True