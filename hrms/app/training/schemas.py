from pydantic import BaseModel
from datetime import date


class TrainingBase(BaseModel):
    employee_id: int
    training_title: str
    training_date: date
    status: str


class TrainingCreate(TrainingBase):
    pass


class TrainingUpdate(BaseModel):
    training_title: str | None = None
    training_date: date | None = None
    status: str | None = None


class TrainingResponse(TrainingBase):
    id: int

    class Config:
        from_attributes = True