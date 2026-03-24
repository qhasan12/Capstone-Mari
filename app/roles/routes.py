from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from math import ceil

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.roles import service, schemas
from app.auth.security import get_current_user

router = APIRouter(tags=["Roles"])


# =====================================================
# CREATE ROLE (SA ONLY)
# =====================================================

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_role(
    data: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    role = service.create_role(db, data, current_user)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Role created successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


# =====================================================
# LIST ROLES
# =====================================================

@router.get("/")
def list_roles(
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    roles, total = service.get_all_roles(
    db,
    current_user,
    page,
    per_page,
    search,
    is_active
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Roles retrieved successfully",
        data={
            "items": [
                schemas.RoleResponse.model_validate(role)
                for role in roles
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page)
        }
    )


# =====================================================
# GET ROLE
# =====================================================

@router.get("/{role_id}", status_code=status.HTTP_200_OK)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    role = service.get_role_by_id(db, role_id, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role retrieved successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


# =====================================================
# UPDATE ROLE (SA ONLY)
# =====================================================

@router.patch("/{role_id}", status_code=status.HTTP_200_OK)
def update_role(
    role_id: int,
    data: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    role = service.update_role(db, role_id, data, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role updated successfully",
        data=schemas.RoleResponse.model_validate(role)
    )


# =====================================================
# DELETE ROLE (SA ONLY)
# =====================================================

@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    role = service.delete_role(db, role_id, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Role deactivated successfully",
        data=schemas.RoleResponse.model_validate(role)
    )