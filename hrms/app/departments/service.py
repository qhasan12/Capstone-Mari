from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Department
from app.hiring.models import HiringRequest
from app.employees.models import Employee
from app.core.rbac import ensure_superadmin

# =========================
# HELPER: ROLE CHECK
# =========================


from sqlalchemy import or_

def get_departments(
    db: Session,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    query = db.query(Department)

    # Active filter
    if is_active is not None:
        query = query.filter(Department.is_active == is_active)

    # Search
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
def get_department_by_id(db: Session, department_id: int):

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

    # RBAC check
    ensure_superadmin(current_user)

    name = data.name.strip()

    existing = db.query(Department).filter(
        Department.name == name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    department = Department(
        name=name,
        is_active=data.is_active if data.is_active is not None else True
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


# =========================
# UPDATE (PATCH)
# =========================
def update_department(db: Session, department_id: int, data, current_user):

    # RBAC check
    ensure_superadmin(current_user)

    department = get_department_by_id(db, department_id)

    update_data = data.model_dump(exclude_unset=True)

    # Handle name uniqueness
    if "name" in update_data:

        new_name = update_data["name"].strip()

        existing = db.query(Department).filter(
            Department.name == new_name,
            Department.id != department_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Department name already in use"
            )

        update_data["name"] = new_name

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


# =========================
# SOFT DELETE
# =========================
def delete_department(db: Session, department_id: int, current_user):

    # RBAC check
    ensure_superadmin(current_user)

    department = get_department_by_id(db, department_id)

    # Prevent deletion if employees exist
    if db.query(Employee).filter(
        Employee.department_id == department_id,
        Employee.is_active == True
    ).first():

        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate department with active employees"
        )

    # Prevent deletion if hiring requests exist
    if db.query(HiringRequest).filter(
        HiringRequest.department_id == department_id
    ).first():

        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate department with hiring requests"
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