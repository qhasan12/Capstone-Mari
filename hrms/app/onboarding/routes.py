from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


# ==========================================
# CREATE
# ==========================================

@router.post("/", response_model=schemas.OnboardingResponse)
def create_onboarding(
    data: schemas.OnboardingCreate,
    db: Session = Depends(get_db)
):
    return service.create_onboarding(db, data)


# ==========================================
# GET BY EMPLOYEE
# ==========================================

@router.get("/{employee_id}", response_model=schemas.OnboardingResponse)
def get_onboarding(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return service.get_onboarding_by_employee(db, employee_id)


# ==========================================
# UPDATE
# ==========================================

@router.put("/{employee_id}", response_model=schemas.OnboardingResponse)
def update_onboarding(
    employee_id: int,
    data: schemas.OnboardingUpdate,
    db: Session = Depends(get_db)
):
    return service.update_onboarding(db, employee_id, data)


# ==========================================
# LIST ALL
# ==========================================

@router.get("/", response_model=list[schemas.OnboardingResponse])
def list_onboarding(
    db: Session = Depends(get_db)
):
    return service.list_onboarding(db)