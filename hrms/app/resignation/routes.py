from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from . import service, schemas

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_resignation(
    data: schemas.ResignationCreate,
    db: Session = Depends(get_db)
):
    resignation = service.create_resignation(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Resignation created successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_resignations(db: Session = Depends(get_db)):
    records = service.get_all_resignations(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignations retrieved successfully",
        data=[
            schemas.ResignationResponse.model_validate(r)
            for r in records
        ]
    )


@router.get("/{resignation_id}", status_code=status.HTTP_200_OK)
def get_resignation(
    resignation_id: int,
    db: Session = Depends(get_db)
):
    resignation = service.get_resignation_by_id(db, resignation_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation retrieved successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.patch("/{resignation_id}", status_code=status.HTTP_200_OK)
def update_resignation(
    resignation_id: int,
    data: schemas.ResignationUpdate,
    db: Session = Depends(get_db)
):
    resignation = service.update_resignation(db, resignation_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation updated successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.delete("/{resignation_id}", status_code=status.HTTP_200_OK)
def delete_resignation(
    resignation_id: int,
    db: Session = Depends(get_db)
):
    service.deactivate_resignation(db, resignation_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation deactivated successfully"
    )


@router.patch("/clearance/{resignation_id}", status_code=status.HTTP_200_OK)
def update_clearance(
    resignation_id: int,
    data: schemas.ClearanceUpdate,
    db: Session = Depends(get_db)
):
    clearance = service.update_clearance(db, resignation_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Clearance updated successfully",
        data=schemas.ClearanceResponse.model_validate(clearance)
    )