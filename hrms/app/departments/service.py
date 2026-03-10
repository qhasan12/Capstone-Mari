from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from .models import Department
from app.hiring.models import HiringRequest
from app.employees.models import Employee
from app.core.rbac import get_current_employee, require_permission
from sqlalchemy import func

# =========================
# READ ALL
# =========================
def get_departments(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "department:view")

    query = db.query(Department)

    if is_active is not None:
        query = query.filter(Department.is_active == is_active)

    if search:
        query = query.filter(
            Department.name.ilike(f"%{search}%")
        )

    total = query.count()

    departments = (
        query
        .order_by(Department.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return departments, total


# =========================
# READ ONE
# =========================
def get_department_by_id(db: Session, department_id: int, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "department:view")

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# =========================
# CREATE
# =========================
def create_department(db: Session, data, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "department:create")

    name = data.name

    existing = db.query(Department).filter(
        func.lower(Department.name) == name.lower()
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    department = Department(
        name=name,
        is_active=data.is_active
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department

# =========================
# UPDATE
# =========================

def update_department(db: Session, department_id: int, data, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "department:update")

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(404, "Department not found")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:

        existing = db.query(Department).filter(
            func.lower(Department.name) == update_data["name"].lower(),
            Department.id != department_id
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


# =========================
# SOFT DELETE
# =========================
def delete_department(db: Session, department_id: int, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "department:delete")

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(404, "Department not found")

    # Prevent deletion if employees exist
    if db.query(Employee).filter(
        Employee.department_id == department_id,
        Employee.is_active == True
    ).first():

        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate department with active employees"
        )
    if db.query(HiringRequest).filter(
        HiringRequest.department_id == department_id,
        HiringRequest.is_active == True
        ).first():
        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate department with active hiring requests"
        )


    if not department.is_active:
        raise HTTPException(
            status_code=400,
            detail="Department already inactive"
        )

    department.is_active = False

    db.commit()
    db.refresh(department)

    return department