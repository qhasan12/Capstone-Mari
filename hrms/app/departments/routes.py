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
def create_department(
    data: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    department = service.create_department(db, data, current_user)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Department created successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


# =========================
# LIST
# =========================
@router.get("/", status_code=status.HTTP_200_OK)
def list_departments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    departments = service.get_departments(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Departments retrieved successfully",
        data=[schemas.DepartmentResponse.model_validate(dep) for dep in departments]
    )


# =========================
# GET ONE
# =========================
@router.get("/{department_id}", status_code=status.HTTP_200_OK)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    department = service.get_department_by_id(db, department_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department retrieved successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


# =========================
# UPDATE
# =========================
@router.patch("/{department_id}", status_code=status.HTTP_200_OK)
def update_department(
    department_id: int,
    data: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    department = service.update_department(db, department_id, data, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department updated successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


# =========================
# DELETE
# =========================
@router.delete("/{department_id}", status_code=status.HTTP_200_OK)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.delete_department(db, department_id, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department deleted successfully"
    )