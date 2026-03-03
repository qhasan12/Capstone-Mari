from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service

router = APIRouter()


@router.post("/", response_model=schemas.TrainingResponse)
def create_training(data: schemas.TrainingCreate, db: Session = Depends(get_db)):
    return service.create_training(db, data)


@router.get("/", response_model=list[schemas.TrainingResponse])
def list_trainings(db: Session = Depends(get_db)):
    return service.get_trainings(db)


@router.get("/{training_id}", response_model=schemas.TrainingResponse)
def get_training(training_id: int, db: Session = Depends(get_db)):
    return service.get_training_by_id(db, training_id)


@router.patch("/{training_id}", response_model=schemas.TrainingResponse)
def update_training(
    training_id: int,
    data: schemas.TrainingUpdate,
    db: Session = Depends(get_db)
):
    return service.update_training(db, training_id, data)


@router.delete("/{training_id}")
def delete_training(training_id: int, db: Session = Depends(get_db)):
    return service.delete_training(db, training_id)