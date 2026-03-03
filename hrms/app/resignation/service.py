from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import psycopg2
from .models import Resignation, ClearanceRecord
# from app.employees.models import Employee


# CREATE
def create_resignation(db: Session, data):
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(Resignation).filter(
        Resignation.employee_id == data.employee_id,
        Resignation.is_active == True
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Resignation already exists")

    resignation = Resignation(
        employee_id=data.employee_id,
        resignation_date=data.resignation_date,
        notice_end_date=data.notice_end_date,
        manager_approved=False,
        status="Pending Approval"
    )

    db.add(resignation)
    db.commit()
    db.refresh(resignation)

    clearance = ClearanceRecord(resignation_id=resignation.id)
    db.add(clearance)
    db.commit()

    return resignation


# GET BY ID
def get_resignation_by_id(db: Session, resignation_id: int):
    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id,
        Resignation.is_active == True
    ).first()

    if not resignation:
        raise HTTPException(status_code=404, detail="Resignation not found")

    return resignation


# GET ALL
def get_all_resignations(db: Session):
    return db.query(Resignation).filter(
        Resignation.is_active == True
    ).all()


# PATCH UPDATE
def update_resignation(db: Session, resignation_id: int, data):
    resignation = get_resignation_by_id(db, resignation_id)

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(resignation, key, value)

    if resignation.manager_approved:
        resignation.status = "Approved"
    else:
        resignation.status = "Pending Approval"

    db.commit()
    db.refresh(resignation)

    return resignation


# SOFT DELETE
def deactivate_resignation(db: Session, resignation_id: int):
    resignation = get_resignation_by_id(db, resignation_id)
    resignation.is_active = False
    db.commit()
    return resignation


# UPDATE CLEARANCE
def update_clearance(db: Session, resignation_id: int, data):
    clearance = db.query(ClearanceRecord).filter(
        ClearanceRecord.resignation_id == resignation_id,
        ClearanceRecord.is_active == True
    ).first()

    if not clearance:
        raise HTTPException(status_code=404, detail="Clearance record not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(clearance, key, value)

    if (
        clearance.laptop_returned and
        clearance.access_revoked and
        clearance.email_deactivated
    ):
        clearance.clearance_completed = True

    db.commit()
    db.refresh(clearance)

    return clearance