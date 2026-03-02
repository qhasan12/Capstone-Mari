from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.roles.schemas import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)
from app.roles import service

router = APIRouter(tags=["Roles"])


# -----------------------
# Create
# -----------------------

@router.post("/", response_model=RoleResponse)
def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    return service.create_role(db, role_data)


# -----------------------
# List
# -----------------------

@router.get("/", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return service.get_all_roles(db)


# -----------------------
# Retrieve
# -----------------------

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return service.get_role_by_id(db, role_id)


# -----------------------
# Update
# -----------------------

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    update_data: RoleUpdate,
    db: Session = Depends(get_db)
):
    return service.update_role(db, role_id, update_data)


# -----------------------
# Delete
# -----------------------

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return service.delete_role(db, role_id)