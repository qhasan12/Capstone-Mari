from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from . import service, schemas

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee = service.create_employee(db, data)

    return APIResponse(
        code=201,
        message="Employee created successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(db: Session = Depends(get_db)):
    employees = service.get_employees(db)

    return APIResponse(
        code=200,
        message="Employees retrieved successfully",
        data=[schemas.EmployeeResponse.model_validate(emp) for emp in employees]
    )


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = service.get_employee_by_id(db, employee_id)

    return APIResponse(
        code=200,
        message="Employee retrieved successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


@router.patch("/{employee_id}", status_code=status.HTTP_200_OK)
def update_employee(
    employee_id: int,
    data: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = service.update_employee(db, employee_id, data)

    return APIResponse(
        code=200,
        message="Employee updated successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )

@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = service.delete_employee(db, employee_id)

    return APIResponse(
        code=200,
        message="Employee deactivated successfully",
        data=schemas.EmployeeResponse.model_validate(employee)
    )