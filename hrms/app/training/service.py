from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models import TrainingRecord
from app.employees.models import Employee


# CREATE
def create_training(db: Session, data):
    # Validate employee exists
    employee = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    training = TrainingRecord(**data.model_dump())

    db.add(training)
    db.commit()
    db.refresh(training)

    return training


# READ ALL
def get_trainings(db: Session):
    trainings = db.query(TrainingRecord).all()
    return trainings


# READ ONE
#is_active is not checked here to allow retrieval of both active and inactive records for auditing purposes.
def get_training_by_id(db: Session, training_id: int):
    training = db.query(TrainingRecord).filter(
        TrainingRecord.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    return training


# UPDATE (PATCH)
def update_training(db: Session, training_id: int, data):
    training = get_training_by_id(db, training_id)

    update_data = data.model_dump(exclude_unset=True)

    # Validate employee if being updated
    if "employee_id" in update_data:
        employee = db.query(Employee).filter(
            Employee.id == update_data["employee_id"]
        ).first()

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

    # Update fields (including is_active if provided)
    for key, value in update_data.items():
        setattr(training, key, value)

    db.commit()
    db.refresh(training)

    return training


# soft delete
def delete_training(db: Session, training_id: int):
    training = get_training_by_id(db, training_id)

    if not training.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Training already inactive"
        )

    training.is_active = False

    db.commit()
    db.refresh(training)

    return training