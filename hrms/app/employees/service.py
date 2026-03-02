from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import Employee
from app.departments.models import Department
from app.roles.models import Role


# CREATE
def create_employee(db: Session, data):
    # Trim name
    full_name = data.full_name.strip()

    # Check duplicate email
    existing = db.query(Employee).filter(Employee.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Validate department
    department = db.query(Department).filter(
        Department.id == data.department_id,
        Department.is_active == True
    ).first()
    if not department:
        raise HTTPException(status_code=400, detail="Invalid or inactive department")

    # Validate role
    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Validate manager
    if data.manager_id:
        manager = db.query(Employee).filter(
            Employee.id == data.manager_id,
            Employee.is_active == True
        ).first()
        if not manager:
            raise HTTPException(status_code=400, detail="Invalid manager")

    employee = Employee(**data.model_dump())
    employee.full_name = full_name

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# READ ALL (only active)
def get_employees(db: Session):
    return db.query(Employee).filter(
        Employee.is_active == True
    ).order_by(Employee.id).all()


# READ ONE
def get_employee_by_id(db: Session, employee_id: int):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# UPDATE
def update_employee(db: Session, employee_id: int, data):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = data.model_dump(exclude_unset=True)

    # Email duplicate check
    if "email" in update_data:
        existing = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.id != employee_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    # Department validation
    if "department_id" in update_data:
        department = db.query(Department).filter(
            Department.id == update_data["department_id"],
            Department.is_active == True
        ).first()
        if not department:
            raise HTTPException(status_code=400, detail="Invalid department")

    # Role validation
    if "role_id" in update_data:
        role = db.query(Role).filter(Role.id == update_data["role_id"]).first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role")

    # Manager validation
    if "manager_id" in update_data and update_data["manager_id"]:
        manager = db.query(Employee).filter(
            Employee.id == update_data["manager_id"],
            Employee.is_active == True
        ).first()
        if not manager:
            raise HTTPException(status_code=400, detail="Invalid manager")

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# SOFT DELETE
def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not employee.is_active:
        raise HTTPException(status_code=400, detail="Employee already inactive")

    employee.is_active = False
    db.commit()
    db.refresh(employee)

    return employee