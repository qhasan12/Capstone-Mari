from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.auth.security import get_current_user

from . import schemas, service


router = APIRouter(tags=["Training"])


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_training(
    data: schemas.TrainingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    training = service.create_training(db, data, current_user)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Training created successfully",
        data=schemas.TrainingResponse.model_validate(training)
    )


# LIST
@router.get("/", status_code=status.HTTP_200_OK)
def list_trainings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    trainings = service.get_trainings(db, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Trainings retrieved successfully",
        data=[schemas.TrainingResponse.model_validate(t) for t in trainings]
    )


# GET ONE
@router.get("/{training_id}", status_code=status.HTTP_200_OK)
def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    training = service.get_training_by_id(db, training_id, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Training retrieved successfully",
        data=schemas.TrainingResponse.model_validate(training)
    )


# UPDATE
@router.patch("/{training_id}", status_code=status.HTTP_200_OK)
def update_training(
    training_id: int,
    data: schemas.TrainingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    training = service.update_training(db, training_id, data, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Training updated successfully",
        data=schemas.TrainingResponse.model_validate(training)
    )


# DELETE
@router.delete("/{training_id}", status_code=status.HTTP_200_OK)
def delete_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.delete_training(db, training_id, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Training deleted successfully",
        data=None
    )