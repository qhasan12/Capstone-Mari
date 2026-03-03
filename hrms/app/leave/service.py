from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from .models import LeaveType, LeaveBalance, LeaveRequest


# =====================================================
# LEAVE TYPES
# =====================================================

def create_leave_type(db: Session, data):
    leave_type = LeaveType(**data.dict())
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type


def get_leave_types(db: Session):
    return db.query(LeaveType).all()


# =====================================================
# LEAVE BALANCE
# =====================================================

def create_leave_balance(db: Session, data):
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


def get_employee_balances(db: Session, employee_id: int):
    return db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee_id
    ).all()


# =====================================================
# LEAVE REQUEST
# =====================================================

def create_leave_request(db: Session, data):
    # Calculate number of leave days
    leave_days = (data.end_date - data.start_date).days + 1

    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid leave dates")

    # Get balance
    balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == data.employee_id,
        LeaveBalance.leave_type_id == data.leave_type_id
    ).first()

    if not balance:
        raise HTTPException(status_code=404, detail="Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    leave_request = LeaveRequest(
        employee_id=data.employee_id,
        leave_type_id=data.leave_type_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="Pending"
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


def update_leave_status(db: Session, leave_id: int, data):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    leave.status = data.status

    # If approved → deduct leaves
    if data.status == "Approved":
        leave_days = (leave.end_date - leave.start_date).days + 1

        balance = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == leave.employee_id,
            LeaveBalance.leave_type_id == leave.leave_type_id
        ).first()

        balance.used_leaves += leave_days
        balance.remaining_leaves -= leave_days

    db.commit()
    db.refresh(leave)

    return leave


def get_leave_requests(db: Session):
    return db.query(LeaveRequest).all()