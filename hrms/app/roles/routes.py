from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import service, schemas

router = APIRouter()


# ==============================
# CREATE
# ==============================

@router.post("/", response_model=schemas.RoleResponse)
def create_role(data: schemas.RoleCreate, db: Session = Depends(get_db)):
    return service.create_role(db, data)


# ==============================
# LIST ALL
# ==============================

@router.get("/", response_model=list[schemas.RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return service.get_roles(db)


# ==============================
# GET BY ID
# ==============================

@router.get("/{role_id}", response_model=schemas.RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return service.get_role_by_id(db, role_id)


# ==============================
# UPDATE
# ==============================

@router.put("/{role_id}", response_model=schemas.RoleResponse)
def update_role(role_id: int, data: schemas.RoleUpdate, db: Session = Depends(get_db)):
    return service.update_role(db, role_id, data)


# ==============================
# DELETE
# ==============================

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return service.delete_role(db, role_id)
