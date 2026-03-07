from sqlalchemy.orm import Session
from fastapi import HTTPException

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

    leave_type = LeaveType(**data.dict())

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


def get_all_leave_types(db: Session, current_user):

    get_current_employee(db, current_user)

    return db.query(LeaveType).filter(
        LeaveType.is_active == True
    ).all()


def update_leave_type(db: Session, leave_type_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403)

    leave_type = get_leave_type_by_id(db, leave_type_id, current_user)

    for key, value in data.dict(exclude_unset=True).items():
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
        remaining_leaves=data.total_leaves
    )

    db.add(balance)
    db.commit()
    db.refresh(balance)

    return balance


def get_employee_balances(db: Session, employee_id: int, current_user):

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

    # everyone can only apply leave for themselves
    if data.employee_id != employee.id:
        raise HTTPException(403, "Can only apply leave for yourself")

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


def get_leave_requests(db: Session, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role in ["SA", "HR"]:
        return db.query(LeaveRequest).filter(
            LeaveRequest.is_active == True
        ).all()

    if role == "MGR":
        return db.query(LeaveRequest).join(Employee).filter(
            (Employee.manager_id == employee.id) |
            (LeaveRequest.employee_id == employee.id),
            LeaveRequest.is_active == True
        ).all()

    if role == "EMP":
        return db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.is_active == True
        ).all()


def update_leave_request(db: Session, leave_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id,
        LeaveRequest.is_active == True
    ).first()

    if not leave:
        raise HTTPException(404, "Leave request not found")

    role = employee.role.title

    # employee can only modify their own leave
    if role == "EMP" and leave.employee_id != employee.id:
        raise HTTPException(403)

    # manager can approve team leave
    if role == "MGR":
        if leave.employee.manager_id != employee.id:
            raise HTTPException(403)

    old_status = leave.status

    for key, value in data.dict(exclude_unset=True).items():
        setattr(leave, key, value)

    leave_days = (leave.end_date - leave.start_date).days + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == leave.employee_id,
        LeaveBalance.leave_type_id == leave.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    # APPROVE
    if old_status != "Approved" and leave.status == "Approved":

        if balance.remaining_leaves < leave_days:
            raise HTTPException(400, "Insufficient leave balance")

        balance.used_leaves += leave_days
        balance.remaining_leaves -= leave_days

    # CANCEL
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

    leave.is_active = False

    db.commit()

    return leave