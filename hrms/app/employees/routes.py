from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.auth.security import get_current_user

from . import service, schemas

router = APIRouter()


# =========================
# CREATE
# =========================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(
    data: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee = service.create_employee(db, data, current_user)

    return APIResponse(
        code=201,
        message="Employee created successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


# =========================
# LIST
# =========================
@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employees = service.get_employees(db, current_user)

    return APIResponse(
        code=200,
        message="Employees retrieved successfully",
        data=[schemas.EmployeeResponse.model_validate(emp) for emp in employees]
    )


# =========================
# GET ONE
# =========================
@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee = service.get_employee_by_id(db, employee_id, current_user)

    return APIResponse(
        code=200,
        message="Employee retrieved successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


# =========================
# UPDATE
# =========================
@router.patch("/{employee_id}", status_code=status.HTTP_200_OK)
def update_employee(
    employee_id: int,
    data: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee = service.update_employee(db, employee_id, data, current_user)

    return APIResponse(
        code=200,
        message="Employee updated successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


# =========================
# DELETE
# =========================
@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee = service.delete_employee(db, employee_id, current_user)

    return APIResponse(
        code=200,
        message="Employee deactivated successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )