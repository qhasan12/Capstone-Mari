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
from math import ceil

@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if page < 1:
        page = 1

    per_page = min(per_page, 100)

    employees, total = service.get_employees(
        db, current_user, page, per_page, search, is_active
    )

    return APIResponse(
        code=200,
        message="Employees retrieved successfully",
        data={
            "items": [
                schemas.EmployeeResponse.model_validate(emp)
                for emp in employees
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page) if per_page else 1
        }
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

@router.post("/agent/query")
def employee_agent(
    query: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.agents.employee.agent_service import handle_query
    return handle_query(query, db, current_user)