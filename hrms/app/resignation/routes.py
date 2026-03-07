from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.auth.security import get_current_user

from . import service, schemas


router = APIRouter(tags=["Resignations"])


# =====================================================
# RESIGNATION
# =====================================================

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_resignation(
    data: schemas.ResignationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    resignation = service.create_resignation(db, data, current_user)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Resignation created successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.get("/", status_code=status.HTTP_200_OK)
def list_resignations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    records = service.get_all_resignations(db, current_user)

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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    resignation = service.get_resignation_by_id(
        db, resignation_id, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation retrieved successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.patch("/{resignation_id}", status_code=status.HTTP_200_OK)
def update_resignation(
    resignation_id: int,
    data: schemas.ResignationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    resignation = service.update_resignation(
        db, resignation_id, data, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation updated successfully",
        data=schemas.ResignationResponse.model_validate(resignation)
    )


@router.delete("/{resignation_id}", status_code=status.HTTP_200_OK)
def delete_resignation(
    resignation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    service.deactivate_resignation(
        db, resignation_id, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Resignation deactivated successfully"
    )


# =====================================================
# CLEARANCE
# =====================================================

@router.get("/clearance", status_code=status.HTTP_200_OK)
def list_clearance(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    records = service.get_all_clearance(db, current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Clearance records retrieved successfully",
        data=[
            schemas.ClearanceResponse.model_validate(c)
            for c in records
        ]
    )


@router.get("/clearance/{resignation_id}", status_code=status.HTTP_200_OK)
def get_clearance(
    resignation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    clearance = service.get_clearance_by_resignation_id(
        db, resignation_id, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Clearance retrieved successfully",
        data=schemas.ClearanceResponse.model_validate(clearance)
    )


@router.patch("/clearance/{resignation_id}", status_code=status.HTTP_200_OK)
def update_clearance(
    resignation_id: int,
    data: schemas.ClearanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    clearance = service.update_clearance(
        db, resignation_id, data, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Clearance updated successfully",
        data=schemas.ClearanceResponse.model_validate(clearance)
    )


@router.delete("/clearance/{resignation_id}", status_code=status.HTTP_200_OK)
def delete_clearance(
    resignation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    service.deactivate_clearance(
        db, resignation_id, current_user
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Clearance deactivated successfully"
    )