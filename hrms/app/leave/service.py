from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from .models import LeaveType, LeaveBalance, LeaveRequest
from app.employees.models import Employee
from app.core.rbac import get_current_employee,require_permission,has_permission


# =====================================================
# LEAVE TYPES
# =====================================================

def create_leave_type(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "leave_type:create")
    leave_type = LeaveType(**data.model_dump())

    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)

    return leave_type


def get_leave_type_by_id(db: Session, leave_type_id: int, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "leave_type:view")

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

    employee=get_current_employee(db, current_user)
    require_permission(db, employee, "leave_type:view")

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

    require_permission(db, employee, "leave_type:update")
    leave_type = get_leave_type_by_id(db, leave_type_id, current_user)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(leave_type, key, value)

    db.commit()
    db.refresh(leave_type)

    return leave_type


def soft_delete_leave_type(db: Session, leave_type_id: int, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "leave_type:delete")
    leave_type = get_leave_type_by_id(db, leave_type_id, current_user)

    leave_type.is_active = False

    db.commit()

    return leave_type


# =====================================================
# LEAVE BALANCES
# =====================================================

def create_leave_balance(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "leave_balance:create")

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
    

    query = db.query(LeaveBalance).join(Employee).join(LeaveType)

    # RBAC
    if has_permission(db, employee, "leave_balance:view"):
        pass

    elif has_permission(db, employee, "leave_balance:view_team"):

        query = query.filter(
            or_(
                Employee.manager_id == employee.id,  # team
                Employee.id == employee.id           # self
            )
        )
        print(query)
    elif has_permission(db, employee, "leave_balance:view_self"):
        query = query.filter(LeaveBalance.employee_id == employee.id)
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

    # RBAC
    if has_permission(db, employee, "leave_balance:view"):
        pass

    elif has_permission(db, employee, "leave_balance:view_team"):

        target = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not target:
            raise HTTPException(404, "Employee not found")

        if target.manager_id != employee.id and employee.id != employee_id:
            raise HTTPException(403, "Not allowed")

    elif has_permission(db, employee, "leave_balance:view_self"):

        if employee.id != employee_id:
            raise HTTPException(403, "Can only view your own balances")

    else:
        raise HTTPException(403, "Not allowed")

    balances = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee_id,
        LeaveBalance.is_active == True
    ).all()

    return balances

from datetime import date

# =====================================================
# LEAVE REQUESTS
# =====================================================
def create_leave_request(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)
    if data.start_date < date.today():
        raise HTTPException(400, "Start date cannot be in the past")

    require_permission(db, employee, "leave_request:create")

    if data.end_date < data.start_date:
        raise HTTPException(400, "End date cannot be before start date")

    leave_days = (data.end_date - data.start_date).days + 1

    # =========================
    # Prevent overlapping leaves
    # =========================

    existing = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.is_active == True,
        LeaveRequest.status != "Rejected",
        LeaveRequest.start_date <= data.end_date,
        LeaveRequest.end_date >= data.start_date,
        LeaveRequest.leave_type_id == data.leave_type_id
    ).first()

    if existing:
        raise HTTPException(
            400,
            "Leave request already exists for the selected dates"
        )

    # =========================
    # Check leave balance
    # =========================

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee.id,
        LeaveBalance.leave_type_id == data.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    if not balance:
        raise HTTPException(404, "Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(400, "Insufficient leave balance")

    # =========================
    # Create request
    # =========================

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
    is_active: bool | None = True
):

    employee = get_current_employee(db, current_user)

    query = db.query(LeaveRequest).join(
        Employee, LeaveRequest.employee_id == Employee.id
    )

    if is_active is not None:
        query = query.filter(LeaveRequest.is_active == is_active)

    # SA / HR → view all
    if has_permission(db, employee, "leave_request:view"):
        pass

    # Manager → team + self
    elif has_permission(db, employee, "leave_request:view_team"):
        query = query.filter(
            (Employee.manager_id == employee.id) |
            (LeaveRequest.employee_id == employee.id)
        )

    # Employee → self
    elif has_permission(db, employee, "leave_request:view_self"):
        query = query.filter(
            LeaveRequest.employee_id == employee.id
        )

    else:
        raise HTTPException(403, "Not allowed")

    total = query.count()

    requests = (
        query
        .order_by(LeaveRequest.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return requests, total

def soft_delete_leave_request(db: Session, leave_id: int, current_user):
    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "leave_request:delete")  # SA/HR only

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(404, "Leave request not found")

    if not leave.is_active:
        raise HTTPException(400, "Leave request already inactive")

    leave.is_active = False

    db.commit()
    db.refresh(leave)

    return leave



def update_leave_request(db: Session, leave_id: int, data, current_user):

    employee = get_current_employee(db, current_user)
    update_data = data.model_dump(exclude_unset=True)

    leave = db.query(LeaveRequest).join(Employee).filter(
        LeaveRequest.id == leave_id,
        LeaveRequest.is_active == True
    ).first()

    if not leave:
        raise HTTPException(404, "Leave request not found")

    old_status = leave.status

    # =====================
    # HR / SA
    # =====================

    if has_permission(db, employee, "leave_request:update"):

        # Cannot approve/reject own leave
        if leave.employee_id == employee.id and update_data.get("status") in ["Approved","Rejected"]:
            raise HTTPException(403, "Cannot approve/reject your own leave")
    # =====================
    # MANAGER
    # =====================

    elif (has_permission(db, employee, "leave_request:approve") or has_permission(db, employee, "leave_request:reject")) and employee.role.title == "MGR":

        # must be team member
        if leave.employee_id == employee.id:
            raise HTTPException(403, "Managers cannot approve their own leave")
        
        if leave.employee.manager_id != employee.id:
            raise HTTPException(403, "Managers can only approve/reject team leave")

        if update_data.get("status") not in ["Approved", "Rejected"]:
            raise HTTPException(403, "Managers can only approve or reject leave")


    # =====================
    # EMPLOYEE OR SELF EDIT
    # =====================

    elif leave.employee_id == employee.id:

        # employees cannot approve/reject
        if update_data.get("status") in ["Approved", "Rejected"]:
            raise HTTPException(403, "Employees cannot approve/reject leave")

        # approved leave cannot be edited except cancel
        if old_status == "Approved" and update_data.get("status") != "Cancelled":
            raise HTTPException(400, "Approved leave cannot be modified")
        if old_status == "Rejected":
            raise HTTPException(400, "Rejected leave cannot be modified")

    else:
        raise HTTPException(403, "Not allowed")

    # =====================
    # CANCEL RULE
    # =====================

    if update_data.get("status") == "Cancelled":

        if not has_permission(db, employee, "leave_request:cancel"):
            raise HTTPException(403)

        # cancel only own leave
        if leave.employee_id != employee.id:
            raise HTTPException(403, "Can only cancel your own leave")

    # =====================
    # APPLY UPDATE
    # =====================

    for key, value in update_data.items():
        setattr(leave, key, value)

    # =====================
    # BALANCE CALCULATION
    # =====================

    leave_days = (leave.end_date - leave.start_date).days + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == leave.employee_id,
        LeaveBalance.leave_type_id == leave.leave_type_id,
        LeaveBalance.is_active == True
    ).first()

    if not balance:
        raise HTTPException(404, "Leave balance not found")

    # approval
    if old_status != "Approved" and leave.status == "Approved":

        if balance.remaining_leaves < leave_days:
            raise HTTPException(400, "Insufficient leave balance")

        balance.used_leaves += leave_days
        balance.remaining_leaves -= leave_days

    # cancellation
    if old_status == "Approved" and leave.status == "Cancelled":

        balance.used_leaves -= leave_days
        balance.remaining_leaves += leave_days
    # status validation
    allowed_status = ["Approved", "Rejected", "Cancelled"]

    if "status" in update_data and update_data["status"] not in allowed_status:
        raise HTTPException(400, "Invalid status update")

    db.commit()
    db.refresh(leave)

    return leave