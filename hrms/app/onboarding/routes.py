from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from math import ceil

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.auth.security import get_current_user

from . import service, schemas

router = APIRouter(tags=["Onboarding"])


# =====================================================
# CREATE
# =====================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_onboarding(
    data: schemas.OnboardingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    onboarding = service.create_onboarding(db, data, current_user)

    return APIResponse(
        code=201,
        message="Onboarding created successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


# =====================================================
# LIST
# =====================================================
@router.get("/", status_code=status.HTTP_200_OK)
def list_onboarding(
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    records, total = service.get_all_onboarding(
        db, current_user, page, per_page, search, is_active
    )

    return APIResponse(
        code=200,
        message="Onboarding records retrieved successfully",
        data={
            "items": [
                schemas.OnboardingResponse.model_validate(record)
                for record in records
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page)
        }
    )


# =====================================================
# GET ONE
# =====================================================
@router.get("/{onboarding_id}", status_code=status.HTTP_200_OK)
def get_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    onboarding = service.get_onboarding_by_id(db, onboarding_id, current_user)

    return APIResponse(
        code=200,
        message="Onboarding retrieved successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


# =====================================================
# UPDATE
# =====================================================
@router.patch("/{onboarding_id}", status_code=status.HTTP_200_OK)
def update_onboarding(
    onboarding_id: int,
    data: schemas.OnboardingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    onboarding = service.update_onboarding(db, onboarding_id, data, current_user)

    return APIResponse(
        code=200,
        message="Onboarding updated successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


# =====================================================
# DELETE
# =====================================================
@router.delete("/{onboarding_id}", status_code=status.HTTP_200_OK)
def delete_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.soft_delete_onboarding(db, onboarding_id, current_user)

    return APIResponse(
        code=200,
        message="Onboarding deleted successfully"
    )