from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Onboarding


# CREATE
def create_onboarding(db: Session, data):
    existing = db.query(Onboarding).filter(
        Onboarding.employee_id == data.employee_id,
        Onboarding.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Onboarding already exists for this employee"
        )

    onboarding = Onboarding(
        employee_id=data.employee_id,
        stage="Initiated"
    )

    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)

    return onboarding


# GET BY ID
def get_onboarding_by_id(db: Session, onboarding_id: int):
    onboarding = db.query(Onboarding).filter(
        Onboarding.id == onboarding_id
    ).first()

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    return onboarding


# GET ALL
def get_all_onboarding(db: Session):
    return db.query(Onboarding).filter(
        Onboarding.is_active == True
    ).all()


# PATCH UPDATE
def update_onboarding(db: Session, onboarding_id: int, data):
    onboarding = get_onboarding_by_id(db, onboarding_id)

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(onboarding, field, value)

    # Smart stage logic
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


# SOFT DELETE
def soft_delete_onboarding(db: Session, onboarding_id: int):
    onboarding = get_onboarding_by_id(db, onboarding_id)
    onboarding.is_active = False
    db.commit()
    return onboarding