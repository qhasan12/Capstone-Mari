from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from .models import TrainingRecord
from app.employees.models import Employee
from app.core.rbac import get_current_employee


# =====================================================
# CREATE
# =====================================================

def create_training(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to create training")

    emp = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not emp:
        raise HTTPException(404, "Employee not found")

    # Prevent duplicates
    existing = db.query(TrainingRecord).filter(
        TrainingRecord.employee_id == data.employee_id,
        TrainingRecord.training_title == data.training_title,
        TrainingRecord.training_date == data.training_date,
        TrainingRecord.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Training record already exists for this employee"
        )

    training = TrainingRecord(
        **data.model_dump(),
        is_active=True
    )

    db.add(training)
    db.commit()
    db.refresh(training)

    return training
# =====================================================
# LIST
# =====================================================

def get_trainings(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    get_current_employee(db, current_user)

    query = db.query(TrainingRecord)

    if is_active is not None:
        query = query.filter(TrainingRecord.is_active == is_active)

    if search:
        query = query.join(Employee).filter(
            or_(
                Employee.full_name.ilike(f"%{search}%"),
                TrainingRecord.training_title.ilike(f"%{search}%")
            )
        )

    total = query.count()

    trainings = (
        query
        .order_by(TrainingRecord.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return trainings, total


# =====================================================
# GET ONE
# =====================================================

def get_training_by_id(db: Session, training_id: int, current_user):

    get_current_employee(db, current_user)

    training = db.query(TrainingRecord).filter(
        TrainingRecord.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    return training


# =====================================================
# UPDATE
# =====================================================

def update_training(db: Session, training_id: int, data, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to update training")

    training = db.query(TrainingRecord).filter(
        TrainingRecord.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    if "employee_id" in update_data:

        emp = db.query(Employee).filter(
            Employee.id == update_data["employee_id"]
        ).first()

        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

    for key, value in update_data.items():
        setattr(training, key, value)

    db.commit()
    db.refresh(training)

    return training


# =====================================================
# DELETE (SOFT DELETE)
# =====================================================

def delete_training(db: Session, training_id: int, current_user):

    employee = get_current_employee(db, current_user)

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to delete training")

    training = db.query(TrainingRecord).filter(
        TrainingRecord.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    if not training.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Training already inactive"
        )

    training.is_active = False

    db.commit()
    db.refresh(training)

    return training