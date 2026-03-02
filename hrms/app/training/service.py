from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import TrainingRecord


def create_training(db: Session, data):
    training = TrainingRecord(**data.dict())
    db.add(training)
    db.commit()
    db.refresh(training)
    return training


def get_trainings(db: Session):
    return db.query(TrainingRecord).all()


def get_training_by_id(db: Session, training_id: int):
    training = db.query(TrainingRecord).filter(
        TrainingRecord.id == training_id
    ).first()

    if not training:
        raise HTTPException(status_code=404, detail="Training not found")

    return training


def update_training(db: Session, training_id: int, data):
    training = get_training_by_id(db, training_id)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(training, key, value)

    db.commit()
    db.refresh(training)
    return training


def delete_training(db: Session, training_id: int):
    training = get_training_by_id(db, training_id)
    db.delete(training)
    db.commit()
    return {"message": "Training deleted successfully"}