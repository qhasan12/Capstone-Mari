from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from .models import LeaveType, LeaveBalance, LeaveRequest
from app.core.rbac import get_current_employee
from app.employees.models import Employee


# =====================================================
# LEAVE TYPES
# =====================================================

def create_leave_type(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed")

    leave_type = LeaveType(**data.model_dump())

    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)

    return leave_type


def get_leave_type_by_id(db: Session, leave_type_id: int, current_user):

    get_current_employee(db, current_user)

    leave_type = db.query(LeaveType).filter(
        LeaveType.id == leave_type_id
    ).first()

    if not leave_type:
        raise HTTPException(404, "Leave type not found")

    return leave_type


def get_all_leave_types(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    get_current_employee(db, current_user)

    query = db.query(LeaveType)

    if is_active is not None:
        query = query.filter(LeaveType.is_active == is_active)

    if search:
        query = query.filter(
            LeaveType.name.ilike(f"%{search}%")
        )

    total = query.count()

    leave_types = (
        query
        .order_by(LeaveType.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return leave_types, total


def update_leave_type(db: Session, leave_type_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    leave_type = get_leave_type_by_id(db, leave_type_id, current_user)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(leave_type, key, value)

    db.commit()
    db.refresh(leave_type)

    return leave_type


def soft_delete_leave_type(db: Session, leave_type_id: int, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    leave_type = get_leave_type_by_id(db, leave_type_id, current_user)

    leave_type.is_active = False

    db.commit()

    return leave_type


# =====================================================
# LEAVE BALANCES
# =====================================================

def create_leave_balance(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    leave_type = db.query(LeaveType).filter(
        LeaveType.id == data.leave_type_id,
        LeaveType.is_active == True
    ).first()

    if not leave_type:
        raise HTTPException(404, "Leave type not found")

    existing = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == data.employee_id,
        LeaveBalance.leave_type_id == data.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    if existing:
        raise HTTPException(400, "Leave balance already exists")

    balance = LeaveBalance(
        employee_id=data.employee_id,
        leave_type_id=data.leave_type_id,
        total_leaves=data.total_leaves,
        used_leaves=0,
        remaining_leaves=data.total_leaves,
        is_active=True
    )

    db.add(balance)
    db.commit()
    db.refresh(balance)

    return balance


# =====================================================
# ALL EMPLOYEE BALANCES (HR DASHBOARD)
# =====================================================

def get_all_balances(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = None
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    query = db.query(LeaveBalance).join(Employee).join(LeaveType)

    # RBAC
    if role in ["SA", "HR"]:
        pass

    elif role == "MGR":
        query = query.filter(
            (Employee.manager_id == employee.id) |
            (Employee.id == employee.id)
        )
    elif role == "EMP":
        query = query.filter(Employee.id == employee.id)

    else:
        raise HTTPException(403, "Not allowed")

    if is_active is not None:
        query = query.filter(LeaveBalance.is_active == is_active)

    if search:
        query = query.filter(
            or_(
                Employee.full_name.ilike(f"%{search}%"),
                LeaveType.name.ilike(f"%{search}%")
            )
        )

    total = query.count()

    balances = (
        query
        .order_by(LeaveBalance.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return balances, total

# =====================================================
# SINGLE EMPLOYEE BALANCES
# =====================================================

def get_employee_balances(
    db: Session,
    employee_id: int,
    current_user
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role == "EMP" and employee.id != employee_id:
        raise HTTPException(403)

    if role == "MGR":

        target = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not target:
            raise HTTPException(404, "Employee not found")

        if employee.id != employee_id and target.manager_id != employee.id:
            raise HTTPException(403)

    balances = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee_id,
        LeaveBalance.is_active == True
    ).all()

    return balances


# =====================================================
# LEAVE REQUESTS
# =====================================================

def create_leave_request(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    if data.employee_id != employee.id:
        raise HTTPException(403, "Can only apply leave for yourself")
    if data.end_date < data.start_date:
        raise HTTPException(400, "End date cannot be before start date")


    leave_days = (data.end_date - data.start_date).days + 1

    if leave_days <= 0:
        raise HTTPException(400, "Invalid leave dates")

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee.id,
        LeaveBalance.leave_type_id == data.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    if not balance:
        raise HTTPException(404, "Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(400, "Insufficient leave balance")

    leave_request = LeaveRequest(
        employee_id=employee.id,
        leave_type_id=data.leave_type_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="Pending",
        is_active=True
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


def get_leave_requests(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    is_active: bool | None = None
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    query = db.query(LeaveRequest)

    if is_active is not None:
        query = query.filter(LeaveRequest.is_active == is_active)

    if role in ["SA", "HR"]:
        pass

    elif role == "MGR":
        query = query.join(Employee).filter(
            (Employee.manager_id == employee.id) |
            (LeaveRequest.employee_id == employee.id)
        )

    elif role == "EMP":
        query = query.filter(
            LeaveRequest.employee_id == employee.id
        )

    total = query.count()

    requests = (
        query
        .order_by(LeaveRequest.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return requests, total


def update_leave_request(db: Session, leave_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id,
        LeaveRequest.is_active == True
    ).first()

    if not leave:
        raise HTTPException(404, "Leave request not found")

    role = employee.role.title
    update_data = data.model_dump(exclude_unset=True)

    # =========================
    # ROLE PERMISSIONS
    # =========================

    if role == "EMP":
        if update_data.get("status") in ["Approved", "Rejected","Pending"]:
            raise HTTPException(403, "Employees cannot approve leave")

    if role == "MGR":
        if leave.employee.manager_id != employee.id:
            raise HTTPException(403)
        allowed_fields = {"status"}
        if update_data.get("status") not in ["Approved", "Rejected"]:
            raise HTTPException(403)

        if not set(update_data.keys()).issubset(allowed_fields):
            raise HTTPException(403, "Managers can only update status")

    # =========================
    # STATUS RULES
    # =========================
    if leave.status == "Rejected":
        raise HTTPException(400, "Rejected leave cannot be modified")

    if leave.status == "Approved" and update_data.get("status") == "Approved":
        raise HTTPException(400, "Leave is already approved")

    old_status = leave.status

    for key, value in update_data.items():
        setattr(leave, key, value)

    # =========================
    # BALANCE CALCULATION
    # =========================
    leave_days = (leave.end_date - leave.start_date).days + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == leave.employee_id,
        LeaveBalance.leave_type_id == leave.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    if not balance:
        raise HTTPException(404, "Leave balance not found")

    # Approve leave
    if old_status != "Approved" and leave.status == "Approved":

        if balance.remaining_leaves < leave_days:
            raise HTTPException(400, "Insufficient leave balance")

        balance.used_leaves += leave_days
        balance.remaining_leaves -= leave_days

    # Cancel leave
    if old_status == "Approved" and leave.status == "Cancelled":

        balance.used_leaves -= leave_days
        balance.remaining_leaves += leave_days

    db.commit()
    db.refresh(leave)

    return leave

def soft_delete_leave_request(db: Session, leave_id: int, current_user):

    employee = get_current_employee(db, current_user)

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(404)

    if employee.role.title == "EMP" and leave.employee_id != employee.id:
        raise HTTPException(403)
    if employee.role.title == "MGR":
        raise HTTPException(403, "Managers cannot delete leave requests")

    leave.is_active = False

    db.commit()

    return leave