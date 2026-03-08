from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from .models import Resignation, ClearanceRecord
from app.employees.models import Employee
from app.core.rbac import get_current_employee


# =====================================================
# RESIGNATION
# =====================================================

def create_resignation(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    if data.employee_id != employee.id:
        raise HTTPException(403, "Can only resign for yourself")

    existing = db.query(Resignation).filter(
        Resignation.employee_id == employee.id,
        Resignation.is_active == True
    ).first()

    if existing:
        raise HTTPException(400, "Active resignation already exists")

    resignation = Resignation(
        employee_id=employee.id,
        resignation_date=data.resignation_date,
        notice_end_date=data.notice_end_date,
        manager_approved=False,
        status="Pending Approval",
        is_active=True
    )

    db.add(resignation)
    db.flush()

    clearance = ClearanceRecord(resignation_id=resignation.id)
    db.add(clearance)

    db.commit()
    db.refresh(resignation)

    return resignation


# -----------------------------------------------------

def get_resignation_by_id(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id,
        Resignation.is_active == True
    ).first()

    if not resignation:
        raise HTTPException(404, "Resignation not found")

    role = employee.role.title

    if role in ["SA", "HR"]:
        return resignation

    if role == "MGR":
        if resignation.employee.manager_id != employee.id:
            raise HTTPException(403)

    if role == "EMP":
        if resignation.employee_id != employee.id:
            raise HTTPException(403)

    return resignation


# -----------------------------------------------------

def get_all_resignations(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    query = db.query(Resignation).filter(
        Resignation.is_active == True
    )

    if role in ["SA", "HR"]:
        pass

    elif role == "MGR":
        query = query.join(Employee).filter(
            Employee.manager_id == employee.id
        )

    elif role == "EMP":
        query = query.filter(
            Resignation.employee_id == employee.id
        )

    total = query.count()

    records = (
        query
        .order_by(Resignation.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return records, total


# -----------------------------------------------------

def update_resignation(db: Session, resignation_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id,
        Resignation.is_active == True
    ).first()

    if not resignation:
        raise HTTPException(404, "Resignation not found")

    role = employee.role.title

    # EMP withdraw
    if role == "EMP":

        if resignation.employee_id != employee.id:
            raise HTTPException(403)

        resignation.status = "Withdrawn"
        resignation.is_active = False

    # MGR approve
    elif role == "MGR":

        if resignation.employee.manager_id != employee.id:
            raise HTTPException(403)

        resignation.manager_approved = True
        resignation.status = "Approved"

    # HR / SA full control
    elif role in ["HR", "SA"]:

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(resignation, key, value)

    db.commit()
    db.refresh(resignation)

    return resignation


# -----------------------------------------------------

def deactivate_resignation(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id,
        Resignation.is_active == True
    ).first()

    if not resignation:
        raise HTTPException(404)

    role = employee.role.title

    # EMP withdraw only
    if role == "EMP":

        if resignation.employee_id != employee.id:
            raise HTTPException(403)

        resignation.status = "Withdrawn"
        resignation.is_active = False

    # HR / SA delete
    elif role in ["HR", "SA"]:

        resignation.is_active = False

    else:
        raise HTTPException(403)

    db.commit()
    db.refresh(resignation)

    return resignation


# =====================================================
# CLEARANCE
# =====================================================

def get_clearance_by_resignation_id(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = db.query(ClearanceRecord).filter(
        ClearanceRecord.resignation_id == resignation_id,
        ClearanceRecord.is_active == True
    ).first()

    if not clearance:
        raise HTTPException(404, "Clearance not found")

    return clearance


# -----------------------------------------------------

def get_all_clearance(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10
):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    query = db.query(ClearanceRecord).filter(
        ClearanceRecord.is_active == True
    )

    total = query.count()

    records = (
        query
        .order_by(ClearanceRecord.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return records, total


# -----------------------------------------------------

def update_clearance(db: Session, resignation_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = get_clearance_by_resignation_id(db, resignation_id, current_user)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(clearance, key, value)

    clearance.clearance_completed = (
        clearance.laptop_returned and
        clearance.access_revoked and
        clearance.email_deactivated
    )

    db.commit()
    db.refresh(clearance)

    return clearance


# -----------------------------------------------------

def deactivate_clearance(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = get_clearance_by_resignation_id(db, resignation_id, current_user)

    clearance.is_active = False

    db.commit()
    db.refresh(clearance)

    return clearance