from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


# =====================================================
# LEAVE TYPES
# =====================================================

@router.post("/types", response_model=schemas.LeaveTypeResponse)
def create_leave_type(data: schemas.LeaveTypeCreate, db: Session = Depends(get_db)):
    return service.create_leave_type(db, data)


@router.get("/types", response_model=list[schemas.LeaveTypeResponse])
def list_leave_types(db: Session = Depends(get_db)):
    return service.get_leave_types(db)


# =====================================================
# LEAVE BALANCES
# =====================================================

@router.post("/balances", response_model=schemas.LeaveBalanceResponse)
def create_leave_balance(data: schemas.LeaveBalanceCreate, db: Session = Depends(get_db)):
    return service.create_leave_balance(db, data)


@router.get("/balances/{employee_id}", response_model=list[schemas.LeaveBalanceResponse])
def get_balances(employee_id: int, db: Session = Depends(get_db)):
    return service.get_employee_balances(db, employee_id)


# =====================================================
# LEAVE REQUESTS
# =====================================================

@router.post("/requests", response_model=schemas.LeaveRequestResponse)
def apply_leave(data: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    return service.create_leave_request(db, data)


@router.put("/requests/{leave_id}", response_model=schemas.LeaveRequestResponse)
def update_leave_status(
    leave_id: int,
    data: schemas.LeaveRequestUpdate,
    db: Session = Depends(get_db)
):
    return service.update_leave_status(db, leave_id, data)


@router.get("/requests", response_model=list[schemas.LeaveRequestResponse])
def list_leave_requests(db: Session = Depends(get_db)):
    return service.get_leave_requests(db)