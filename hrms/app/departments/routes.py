from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from . import service, schemas

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_department(
    data: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    department = service.create_department(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Department created successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_departments(db: Session = Depends(get_db)):
    departments = service.get_departments(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Departments retrieved successfully",
        data=[schemas.DepartmentResponse.model_validate(dep) for dep in departments]
    )


@router.get("/{department_id}", status_code=status.HTTP_200_OK)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = service.get_department_by_id(db, department_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department retrieved successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


@router.put("/{department_id}", status_code=status.HTTP_200_OK)
def update_department(
    department_id: int,
    data: schemas.DepartmentUpdate,
    db: Session = Depends(get_db)
):
    department = service.update_department(db, department_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department updated successfully",
        data=schemas.DepartmentResponse.model_validate(department)
    )


@router.delete("/{department_id}", status_code=status.HTTP_200_OK)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    service.delete_department(db, department_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Department deleted successfully"
    )