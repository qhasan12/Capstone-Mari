from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


@router.post("/", response_model=schemas.DepartmentResponse)
def create_department(data: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return service.create_department(db, data)


@router.get("/", response_model=list[schemas.DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return service.get_departments(db)


@router.get("/{department_id}", response_model=schemas.DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    return service.get_department_by_id(db, department_id)


@router.put("/{department_id}", response_model=schemas.DepartmentResponse)
def update_department(department_id: int, data: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    return service.update_department(db, department_id, data)


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    return service.delete_department(db, department_id)