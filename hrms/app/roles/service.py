from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import psycopg2
from .models import Role


# =====================================
# CREATE ROLE
# =====================================

def create_role(db: Session, data):
    role = Role(**data.dict())

    try:
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    except IntegrityError as e:
        db.rollback()

        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(status_code=400, detail="Role title already exists")

        raise HTTPException(status_code=400, detail="Database integrity error")


# =====================================
# GET ALL ROLES
# =====================================

def get_roles(db: Session):
    return db.query(Role).order_by(Role.id).all()


# =====================================
# GET ROLE BY ID
# =====================================

def get_role_by_id(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# =====================================
# UPDATE ROLE
# =====================================

def update_role(db: Session, role_id: int, data):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(role, key, value)

    try:
        db.commit()
        db.refresh(role)
        return role

    except IntegrityError as e:
        db.rollback()

        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(status_code=400, detail="Role title already exists")

        raise HTTPException(status_code=400, detail="Database integrity error")


# =====================================
# DELETE ROLE
# =====================================

def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()

    return {"message": "Role deleted successfully"}