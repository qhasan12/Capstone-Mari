from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.roles.models import Role
from app.roles.schemas import RoleCreate, RoleUpdate


# -----------------------
# Create Role
# -----------------------

def create_role(db: Session, role_data: RoleCreate):
    existing = db.query(Role).filter(Role.title == role_data.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(**role_data.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# -----------------------
# Get All
# -----------------------

def get_all_roles(db: Session):
    return db.query(Role).all()


# -----------------------
# Get By ID
# -----------------------

def get_role_by_id(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# -----------------------
# Update
# -----------------------

def update_role(db: Session, role_id: int, update_data: RoleUpdate):
    role = get_role_by_id(db, role_id)

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)
    return role


# -----------------------
# Delete
# -----------------------

def delete_role(db: Session, role_id: int):
    role = get_role_by_id(db, role_id)

    db.delete(role)
    db.commit()

    return {"message": "Role deleted successfully"}