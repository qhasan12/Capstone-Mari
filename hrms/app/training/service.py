from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .models import TrainingRecord
from app.employees.models import Employee
from app.core.rbac import get_current_employee


# CREATE
def create_training(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to create training")

    emp = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not emp:
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
def get_trainings(db: Session, current_user):

    # Everyone logged in can view
    get_current_employee(db, current_user)

    trainings = db.query(TrainingRecord).all()
    return trainings


# READ ONE
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


# UPDATE
def update_training(db: Session, training_id: int, data, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
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


# DELETE (SOFT DELETE)
def delete_training(db: Session, training_id: int, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
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