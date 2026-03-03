from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


# ==========================================
# CREATE
# ==========================================

@router.post("/", response_model=schemas.ResignationResponse)
def create_resignation(
    data: schemas.ResignationCreate,
    db: Session = Depends(get_db)
):
    return service.create_resignation(db, data)


# ==========================================
# GET BY EMPLOYEE
# ==========================================

@router.get("/{employee_id}", response_model=schemas.ResignationResponse)
def get_resignation(employee_id: int, db: Session = Depends(get_db)):
    return service.get_resignation_by_employee(db, employee_id)


# ==========================================
# UPDATE (Manager Approval)
# ==========================================

@router.put("/{employee_id}", response_model=schemas.ResignationResponse)
def update_resignation(
    employee_id: int,
    data: schemas.ResignationUpdate,
    db: Session = Depends(get_db)
):
    return service.update_resignation(db, employee_id, data)


# ==========================================
# UPDATE CLEARANCE
# ==========================================

@router.put("/clearance/{resignation_id}", response_model=schemas.ClearanceResponse)
def update_clearance(
    resignation_id: int,
    data: schemas.ClearanceUpdate,
    db: Session = Depends(get_db)
):
    return service.update_clearance(db, resignation_id, data)


# ==========================================
# LIST ALL
# ==========================================

@router.get("/", response_model=list[schemas.ResignationResponse])
def list_resignations(db: Session = Depends(get_db)):
    return service.list_resignations(db)