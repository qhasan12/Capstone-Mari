from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .models import Employee
 

# CREATE
def create_employee(db, data):
    employee = Employee(**data.dict())
 
    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
 
 
# READ ALL
def get_employees(db):
    return db.query(Employee).order_by(Employee.id).all()
 
 
# READ ONE
def get_employee_by_id(db, employee_id: int):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )
 
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
 
    return employee
 
 
# UPDATE
def update_employee(db, employee_id: int, data):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )
 
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
 
    for key, value in data.dict(exclude_unset=True).items():
        setattr(employee, key, value)
 
    try:
        db.commit()
        db.refresh(employee)
        return employee
 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
 
 
# DELETE
def delete_employee(db, employee_id: int):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )
 
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
 
    db.delete(employee)
    db.commit()
 
    return {"message": "Employee deleted successfully"}