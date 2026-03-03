from fastapi import APIRouter, Depends
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(data: schemas.EmployeeCreate, db=Depends(get_db)):
    return service.create_employee(db, data)


@router.get("/", response_model=list[schemas.EmployeeResponse])
def list_employees(db=Depends(get_db)):
    return service.get_employees(db)


@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db=Depends(get_db)):
    return service.get_employee_by_id(db, employee_id)


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, data: schemas.EmployeeUpdate, db=Depends(get_db)):
    return service.update_employee(db, employee_id, data)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db=Depends(get_db)):
    return service.delete_employee(db, employee_id)