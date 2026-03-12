from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional


def normalize_name(value: str | None):
    if value is None:
        return value

    if not value:
        raise ValueError("Department name cannot be empty")

    return value


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    is_active: Optional[bool] = True

    model_config = ConfigDict(str_strip_whitespace=True)

    _validate_name = field_validator("name")(normalize_name)


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    # is_active: Optional[bool] = None

    model_config = ConfigDict(str_strip_whitespace=True)

    _validate_name = field_validator("name")(normalize_name)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)