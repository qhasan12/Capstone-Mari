from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from . import service, schemas

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_onboarding(
    data: schemas.OnboardingCreate,
    db: Session = Depends(get_db)
):
    onboarding = service.create_onboarding(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Onboarding created successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_onboarding(db: Session = Depends(get_db)):
    records = service.get_all_onboarding(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Onboarding records retrieved successfully",
        data=[
            schemas.OnboardingResponse.model_validate(o)
            for o in records
        ]
    )


@router.get("/{onboarding_id}", status_code=status.HTTP_200_OK)
def get_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db)
):
    onboarding = service.get_onboarding_by_id(db, onboarding_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Onboarding retrieved successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


@router.patch("/{onboarding_id}", status_code=status.HTTP_200_OK)
def update_onboarding(
    onboarding_id: int,
    data: schemas.OnboardingUpdate,
    db: Session = Depends(get_db)
):
    onboarding = service.update_onboarding(db, onboarding_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Onboarding updated successfully",
        data=schemas.OnboardingResponse.model_validate(onboarding)
    )


@router.delete("/{onboarding_id}", status_code=status.HTTP_200_OK)
def delete_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db)
):
    service.soft_delete_onboarding(db, onboarding_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Onboarding deleted successfully"
    )