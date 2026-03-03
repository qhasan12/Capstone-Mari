from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Onboarding


# ==========================================
# CREATE ONBOARDING RECORD
# ==========================================

def create_onboarding(db: Session, data):
    # Check if onboarding already exists
    existing = db.query(Onboarding).filter(
        Onboarding.employee_id == data.employee_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Onboarding already exists for this employee"
        )

    onboarding = Onboarding(
        employee_id=data.employee_id,
        appointment_letter_generated=False,
        email_created=False,
        resources_allocated=False,
        orientation_sent=False,
        stage="Initiated"
    )

    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)

    return onboarding


# ==========================================
# GET ONBOARDING BY EMPLOYEE
# ==========================================

def get_onboarding_by_employee(db: Session, employee_id: int):
    onboarding = db.query(Onboarding).filter(
        Onboarding.employee_id == employee_id
    ).first()

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    return onboarding


# ==========================================
# UPDATE ONBOARDING PROGRESS
# ==========================================

def update_onboarding(db: Session, employee_id: int, data):
    onboarding = db.query(Onboarding).filter(
        Onboarding.employee_id == employee_id
    ).first()

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(onboarding, field, value)

    # 🔥 Optional Smart Stage Logic
    if onboarding.orientation_sent:
        onboarding.stage = "Completed"
    elif onboarding.resources_allocated:
        onboarding.stage = "Resources Allocated"
    elif onboarding.email_created:
        onboarding.stage = "Email Created"
    elif onboarding.appointment_letter_generated:
        onboarding.stage = "Appointment Generated"

    db.commit()
    db.refresh(onboarding)

    return onboarding


# ==========================================
# LIST ALL ONBOARDING RECORDS
# ==========================================

def list_onboarding(db: Session):
    return db.query(Onboarding).all()