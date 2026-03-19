from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class AssignTargets(BaseModel):

    employees: list[int] | None = None
    departments: list[int] | None = None
    roles: list[int] | None = None
    managers: list[int] | None = None
    all_employees: bool = False


class TrainingBase(BaseModel):
    title: str
    description: Optional[str] = None
    training_date: date


class TrainingCreate(TrainingBase):
    assign_to: AssignTargets


class TrainingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    training_date: Optional[date] = None
    is_active: Optional[bool] = None


class TrainingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    training_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True