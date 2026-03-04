from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from app.roles import service, schemas

router = APIRouter(tags=["Roles"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_role(data: schemas.RoleCreate, db: Session = Depends(get_db)):
    role = service.create_role(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Role created successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_roles(db: Session = Depends(get_db)):
    roles = service.get_all_roles(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Roles retrieved successfully",
        data=[schemas.RoleResponse.model_validate(r) for r in roles]
    )


@router.get("/{role_id}", status_code=status.HTTP_200_OK)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = service.get_role_by_id(db, role_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role retrieved successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


@router.patch("/{role_id}", status_code=status.HTTP_200_OK)
def update_role(role_id: int, data: schemas.RoleUpdate, db: Session = Depends(get_db)):
    role = service.update_role(db, role_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role updated successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = service.delete_role(db, role_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role deactivated successfully",
        data=schemas.RoleResponse.model_validate(role)
    )