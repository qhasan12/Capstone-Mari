from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.roles.models import Role
from app.employees.models import Employee
from app.core.rbac import (
    ensure_superadmin,
    get_current_employee,
    require_permission
)


# =====================================================
# CREATE ROLE
# =====================================================

def create_role(db: Session, role_data, current_user):

    # ensure_superadmin(current_user)

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "role:create")

    title = role_data.title.strip()

    existing = db.query(Role).filter(
        Role.title == title
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )

    role = Role(
        title=title,
        level=role_data.level,
        description=role_data.description,
        is_active=role_data.is_active if role_data.is_active is not None else True
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


# =====================================================
# GET ALL ROLES
# =====================================================

def get_all_roles(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "role:view")

    # SAFETY FIX
    page = page or 1
    per_page = per_page or 10

    query = db.query(Role)

    if is_active is not None:
        query = query.filter(Role.is_active == is_active)

    if search:
        query = query.filter(Role.title.ilike(f"%{search}%"))

    total = query.count()

    roles = (
        query
        .order_by(Role.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return roles, total


# =====================================================
# GET ROLE BY ID
# =====================================================

def get_role_by_id(db: Session, role_id: int, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "role:view")

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(404, "Role not found")

    return role

# =====================================================
# UPDATE ROLE
# =====================================================

def update_role(db: Session, role_id: int, update_data, current_user):

    # ensure_superadmin(current_user)
    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "role:update")

    role = get_role_by_id(db, role_id, current_user)

    data = update_data.model_dump(exclude_unset=True, exclude_none=True)

    if "title" in data:

        data["title"] = data["title"].strip()

        existing = db.query(Role).filter(
            Role.title == data["title"],
            Role.id != role_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Role title already in use"
            )

    for key, value in data.items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)

    return role


# =====================================================
# DELETE ROLE (SOFT DELETE)
# =====================================================

def delete_role(db: Session, role_id: int, current_user):

    # ensure_superadmin(current_user)
    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "role:delete")

    role = get_role_by_id(db, role_id, current_user)

    if not role.is_active:
        raise HTTPException(
            status_code=400,
            detail="Role already inactive"
        )

    active_employee = db.query(Employee).filter(
        Employee.role_id == role_id,
        Employee.is_active == True
    ).first()

    if active_employee:
        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate role assigned to active employees"
        )

    role.is_active = False

    db.commit()
    db.refresh(role)

    return role