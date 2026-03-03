from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import psycopg2
from .models import Resignation, ClearanceRecord
from app.employees.models import Employee


# ==========================================
# CREATE RESIGNATION
# ==========================================

def create_resignation(db: Session, data):
    # Check employee exists
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    resignation = Resignation(
        employee_id=data.employee_id,
        resignation_date=data.resignation_date,
        notice_end_date=data.notice_end_date,
        manager_approved=False,
        status="Pending Approval"
    )

    try:
        db.add(resignation)
        db.commit()
        db.refresh(resignation)

        # Auto-create clearance record
        clearance = ClearanceRecord(
            resignation_id=resignation.id
        )
        db.add(clearance)
        db.commit()

        return resignation

    except IntegrityError as e:
        db.rollback()

        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="Resignation already exists for this employee"
            )

        raise HTTPException(status_code=400, detail="Database integrity error")


# ==========================================
# GET RESIGNATION BY EMPLOYEE
# ==========================================

def get_resignation_by_employee(db: Session, employee_id: int):
    resignation = db.query(Resignation).filter(
        Resignation.employee_id == employee_id
    ).first()

    if not resignation:
        raise HTTPException(status_code=404, detail="Resignation not found")

    return resignation


# ==========================================
# UPDATE RESIGNATION (Approval)
# ==========================================

def update_resignation(db: Session, employee_id: int, data):
    resignation = db.query(Resignation).filter(
        Resignation.employee_id == employee_id
    ).first()

    if not resignation:
        raise HTTPException(status_code=404, detail="Resignation not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(resignation, key, value)

    # Auto status update
    if resignation.manager_approved:
        resignation.status = "Approved"
    else:
        resignation.status = "Pending Approval"

    db.commit()
    db.refresh(resignation)

    return resignation


# ==========================================
# UPDATE CLEARANCE
# ==========================================

def update_clearance(db: Session, resignation_id: int, data):
    clearance = db.query(ClearanceRecord).filter(
        ClearanceRecord.resignation_id == resignation_id
    ).first()

    if not clearance:
        raise HTTPException(status_code=404, detail="Clearance record not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(clearance, key, value)

    # Auto complete logic
    if (
        clearance.laptop_returned and
        clearance.access_revoked and
        clearance.email_deactivated
    ):
        clearance.clearance_completed = True

    db.commit()
    db.refresh(clearance)

    return clearance


# ==========================================
# LIST ALL RESIGNATIONS
# ==========================================

def list_resignations(db: Session):
    return db.query(Resignation).all()