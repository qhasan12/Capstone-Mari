from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Department


# CREATE
def create_department(db: Session, data):
    existing = db.query(Department).filter(Department.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")

    department = Department(name=data.name)
    db.add(department)
    db.commit()
    db.refresh(department)

    return department


# READ ALL
def get_departments(db: Session):
    return db.query(Department).order_by(Department.id).all()


# READ ONE
def get_department_by_id(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


# UPDATE
def update_department(db: Session, department_id: int, data):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    if data.name:
        department.name = data.name

    db.commit()
    db.refresh(department)

    return department


# DELETE
def delete_department(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}