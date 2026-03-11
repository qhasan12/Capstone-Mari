from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from .models import Resignation, ClearanceRecord
from app.employees.models import Employee
from app.core.rbac import get_current_employee,require_permission,has_permission


# =====================================================
# RESIGNATION
# =====================================================

def create_resignation(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)
    if has_permission(db, employee,"resignation:create"):
        if employee.id == data.employee_id:
            pass
    else:
        raise HTTPException(403,"You can only resign for yourself")
    
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

    # Must have at least some view permission
    if not (
        has_permission(db, employee, "resignation:view") or
        has_permission(db, employee, "resignation:view_team") or
        has_permission(db, employee, "resignation:view_self")
    ):
        raise HTTPException(403, "Permission denied")

    resignation = db.query(Resignation).filter(
        Resignation.id == resignation_id,
        Resignation.is_active == True
    ).first()

    if not resignation:
        raise HTTPException(404, "Resignation not found")

    # Full access
    if has_permission(db, employee, "resignation:view"):
        return resignation

    # Team access
    if has_permission(db, employee, "resignation:view_team"):
        if resignation.employee.manager_id != employee.id and resignation.employee_id != employee.id:
            raise HTTPException(403, "You can only view resignations of your team or yourself")
        return resignation

    # Self access
    if has_permission(db, employee, "resignation:view_self"):
        if resignation.employee_id != employee.id:
            raise HTTPException(403, "You can only view your own resignation")
        return resignation

    raise HTTPException(403,"Permission denied")


# -----------------------------------------------------

def get_all_resignations(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    is_active: bool | None = None
):

    employee = get_current_employee(db, current_user)

    # Base query
    query = db.query(Resignation)

    # is_active filter
    if is_active is None:
        query = query.filter(Resignation.is_active == True)
    else:
        query = query.filter(Resignation.is_active == is_active)

    # =================================================
    # RBAC SCOPE
    # =================================================

    if has_permission(db, employee, "resignation:view"):
        pass

    elif has_permission(db, employee, "resignation:view_team"):
        query = query.join(Employee).filter(
            Employee.manager_id == employee.id
        )

    elif has_permission(db, employee, "resignation:view_self"):
        query = query.filter(
            Resignation.employee_id == employee.id
        )

    else:
        raise HTTPException(403, "Permission denied")

    # =================================================
    # PAGINATION
    # =================================================

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

    # =====================================================
    # EMPLOYEE WITHDRAW
    # =====================================================
    if has_permission(db, employee, "resignation:withdraw"):

        if resignation.employee_id != employee.id:
            raise HTTPException(403, "You can only withdraw your own resignation")

        if resignation.status == "Withdrawn":
            raise HTTPException(400, "Resignation already withdrawn")

        resignation.status = "Withdrawn"
        resignation.is_active = False

    # =====================================================
    # MANAGER APPROVE / REJECT
    # =====================================================
    elif has_permission(db, employee, "resignation:approve") or has_permission(db, employee, "resignation:reject"):

        if resignation.employee.manager_id != employee.id:
            raise HTTPException(403, "You can only approve/reject resignations of your team")

        update_data = data.model_dump(exclude_unset=True)

        if "status" in update_data:
            if update_data["status"] not in ["Approved", "Rejected"]:
                raise HTTPException(400, "Manager can only approve or reject")

            resignation.status = update_data["status"]
            resignation.manager_approved = update_data["status"] == "Approved"

    # =====================================================
    # HR / SA UPDATE
    # =====================================================
    elif has_permission(db, employee, "resignation:update"):

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(resignation, key, value)

    else:
        raise HTTPException(403, "Permission denied")

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
    require_permission(db, employee,"clearance:view")

    clearance = db.query(ClearanceRecord).filter(
        ClearanceRecord.resignation_id == resignation_id,
        ClearanceRecord.is_active == True
    ).first()

    if not clearance:
        raise HTTPException(404, "Clearance not found")

    resignation = clearance.resignation
    role = employee.role.title

    if role in ["SA", "HR"]:
        return clearance

    if role == "MGR":
        if resignation.employee.manager_id != employee.id:
            raise HTTPException(403)

    if role == "EMP":
        if resignation.employee_id != employee.id:
            raise HTTPException(403)

    return clearance


# -----------------------------------------------------

def get_all_clearance(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10
):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee,"clearance:view")

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
    require_permission(db, employee,"clearance:update")

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
    require_permission(db, employee,"clearance:delete")

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    clearance = get_clearance_by_resignation_id(db, resignation_id, current_user)

    clearance.is_active = False

    db.commit()
    db.refresh(clearance)

    return clearance