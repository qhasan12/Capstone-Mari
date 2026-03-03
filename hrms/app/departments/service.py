from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Department
from app.hiring.models import HiringRequest
from app.employees.models import Employee  # Ensure Employee model is imported

# READ ALL
def get_departments(db: Session):
    return db.query(Department).filter(
        Department.is_active == True
    ).order_by(Department.id).all()
# READ ONE
def get_department_by_id(db: Session, department_id: int):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    if not department.is_active:
        raise HTTPException(status_code=400, detail="Department is inactive")

    return department
# CREATE
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Department
from app.hiring.models import HiringRequest
from app.employees.models import Employee  # Ensure Employee model is imported

# READ ALL
def get_departments(db: Session):
    return db.query(Department).filter(
        Department.is_active == True
    ).order_by(Department.id).all()
# READ ONE
def get_department_by_id(db: Session, department_id: int):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    if not department.is_active:
        raise HTTPException(status_code=400, detail="Department is inactive")

    return department
# CREATE
def create_department(db: Session, data):
    # Trim and normalize name
    data.name = data.name.strip()

    existing = db.query(Department).filter(Department.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")

    # Default to active if not provided
    is_active = data.is_active if data.is_active is not None else True

    department = Department(name=data.name, is_active=is_active)
    db.add(department)
    db.commit()
    db.refresh(department)

    return department

# UPDATE
def update_department(db: Session, department_id: int, data):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle name separately for duplicate check
    if "name" in update_data:
        update_data["name"] = update_data["name"].strip()

        existing = db.query(Department).filter(
            Department.name == update_data["name"],
            Department.id != department_id  # 🔥 important fix
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Department name already in use"
            )

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department
# # DELETE
def delete_department(db: Session, department_id: int):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if employees are assigned to this department
    existing_employees = db.query(Employee).filter(Employee.department_id == department_id).first()
    if existing_employees:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department with assigned employees"
        )

    # Check if hiring requests exist for this department
    existing_requests = db.query(HiringRequest).filter(HiringRequest.department_id == department_id).first()
    if existing_requests:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department with active hiring requests"
        )


    if not department.is_active:
        raise HTTPException(status_code=400, detail="Department already inactive")
    

    department.is_active = False
    db.commit()
    db.refresh(department)

    return department

# UPDATE
def update_department(db: Session, department_id: int, data):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Handle name update only if provided
    if data.name:
        data.name = data.name.strip()
        # Check if the new name already exists (to prevent duplicates)
        existing = db.query(Department).filter(Department.name == data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Department name already in use")
        department.name = data.name

    # Update is_active only if provided
    if data.is_active is not None:
        department.is_active = data.is_active

    db.commit()
    db.refresh(department)

    return department

# # DELETE
def delete_department(db: Session, department_id: int):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if employees are assigned to this department
    existing_employees = db.query(Employee).filter(Employee.department_id == department_id).first()
    if existing_employees:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department with assigned employees"
        )

    # Check if hiring requests exist for this department
    existing_requests = db.query(HiringRequest).filter(HiringRequest.department_id == department_id).first()
    if existing_requests:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department with active hiring requests"
        )


    if not department.is_active:
        raise HTTPException(status_code=400, detail="Department already inactive")
    

    department.is_active = False
    db.commit()
    db.refresh(department)

    return department