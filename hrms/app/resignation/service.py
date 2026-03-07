from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Resignation, ClearanceRecord
from app.employees.models import Employee
from app.core.rbac import get_current_employee


# =====================================================
# RESIGNATION
# =====================================================

def create_resignation(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    # Everyone can resign but only for themselves
    if data.employee_id != employee.id:
        raise HTTPException(403, "Can only create resignation for yourself")

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
        status="Pending Approval"
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
        if resignation.employee.manager_id != employee.id and resignation.employee_id != employee.id:
            raise HTTPException(403)

    if role == "EMP":
        if resignation.employee_id != employee.id:
            raise HTTPException(403)

    return resignation


# -----------------------------------------------------

def get_all_resignations(db: Session, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role in ["SA", "HR"]:
        return db.query(Resignation).filter(
            Resignation.is_active == True
        ).all()

    if role == "MGR":
        return db.query(Resignation).join(Employee).filter(
            (Employee.manager_id == employee.id) |
            (Resignation.employee_id == employee.id),
            Resignation.is_active == True
        ).all()

    if role == "EMP":
        return db.query(Resignation).filter(
            Resignation.employee_id == employee.id,
            Resignation.is_active == True
        ).all()


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

    # Employee withdraw
    if role == "EMP":

        if resignation.employee_id != employee.id:
            raise HTTPException(403)

        resignation.status = "Withdrawn"
        resignation.is_active = False

    # Manager approval
    elif role == "MGR":

        if resignation.employee.manager_id != employee.id:
            raise HTTPException(403)

        resignation.manager_approved = True
        resignation.status = "Approved"

    # HR / SA full update
    elif role in ["HR", "SA"]:

        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(resignation, key, value)

    db.commit()
    db.refresh(resignation)

    return resignation


# -----------------------------------------------------

def deactivate_resignation(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id
    ).first()

    if not resignation:
        raise HTTPException(404)

    role = employee.role.title

    # Employee or Manager withdraw their own resignation
    if role in ["EMP", "MGR"]:

        if resignation.employee_id != employee.id:
            raise HTTPException(403)

        resignation.status = "Withdrawn"
        resignation.is_active = False

    # HR / SA delete any resignation
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

    clearance = db.query(ClearanceRecord).filter(
        ClearanceRecord.resignation_id == resignation_id,
        ClearanceRecord.is_active == True
    ).first()

    if not clearance:
        raise HTTPException(404, "Clearance record not found")

    role = employee.role.title
    target_employee = clearance.resignation.employee

    if role in ["SA", "HR"]:
        return clearance

    if role == "MGR":
        if target_employee.manager_id != employee.id and target_employee.id != employee.id:
            raise HTTPException(403)

    if role == "EMP":
        if target_employee.id != employee.id:
            raise HTTPException(403)

    return clearance

# -----------------------------------------------------

def update_clearance(db: Session, resignation_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = get_clearance_by_resignation_id(db, resignation_id, current_user)

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(clearance, key, value)

    # auto-complete clearance
    if (
        clearance.laptop_returned and
        clearance.access_revoked and
        clearance.email_deactivated
    ):
        clearance.clearance_completed = True
    else:
        clearance.clearance_completed = False

    db.commit()
    db.refresh(clearance)

    return clearance


# -----------------------------------------------------
def get_all_clearance(db: Session, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role in ["SA", "HR"]:
        return db.query(ClearanceRecord).filter(
            ClearanceRecord.is_active == True
        ).all()

    if role == "MGR":
        return db.query(ClearanceRecord).join(Resignation).join(Employee).filter(
            (Employee.manager_id == employee.id) |
            (Resignation.employee_id == employee.id),
            ClearanceRecord.is_active == True
        ).all()

    if role == "EMP":
        return db.query(ClearanceRecord).join(Resignation).filter(
            Resignation.employee_id == employee.id,
            ClearanceRecord.is_active == True
        ).all()
#------------------------------------------------------

def deactivate_clearance(db: Session, resignation_id: int, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = get_clearance_by_resignation_id(db, resignation_id, current_user)

    clearance.is_active = False

    db.commit()
    db.refresh(clearance)

    return clearance