from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.roles.models import Role
from app.employees.models import Employee
from app.core.rbac import ensure_superadmin

# CREATE
#Qamar;s comment: Added duplicate title check and default is_active to True if not provided
def test1():
    return 1+2
def create_role(db: Session, role_data, current_user):
    ensure_superadmin(current_user)

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


# READ ALL (only active)
def get_all_roles(db: Session):
    return (
        db.query(Role)
        .filter(Role.is_active == True)
        .order_by(Role.id)
        .all()
    )


# READ ONE
def get_role_by_id(db: Session, role_id: int):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


# UPDATE (PATCH style)
def update_role(db: Session, role_id: int, update_data, current_user):
    ensure_superadmin(current_user)

    role = get_role_by_id(db, role_id)

    data = update_data.model_dump(exclude_unset=True)

    # Handle title separately for duplicate protection
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


# SOFT DELETE
def delete_role(db: Session, role_id: int, current_user):
    ensure_superadmin(current_user)
    role = get_role_by_id(db, role_id)

    if not role.is_active:
        raise HTTPException(
            status_code=400,
            detail="Role already inactive"
        )

    # Business rule: prevent deactivation if active employees exist
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
