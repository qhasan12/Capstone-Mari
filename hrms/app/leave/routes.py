from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from math import ceil

from app.core.database import get_db
from app.common.schemas import APIResponse
from app.auth.security import get_current_user

from . import service, schemas

router = APIRouter(tags=["Leave"])


# =====================================================
# LEAVE TYPES
# =====================================================

@router.post("/types", status_code=status.HTTP_201_CREATED)
def create_leave_type(
    data: schemas.LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = service.create_leave_type(db, data, current_user)

    return APIResponse(
        code=201,
        message="Leave type created successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.get("/types", status_code=status.HTTP_200_OK)
def list_leave_types(
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    leave_types, total = service.get_all_leave_types(
        db, current_user, page, per_page, search, is_active
    )

    return APIResponse(
        code=200,
        message="Leave types retrieved successfully",
        data={
            "items": [
                schemas.LeaveTypeResponse.model_validate(lt)
                for lt in leave_types
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page)
        }
    )


@router.get("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def get_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = service.get_leave_type_by_id(
        db, leave_type_id, current_user
    )

    return APIResponse(
        code=200,
        message="Leave type retrieved successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.patch("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def update_leave_type(
    leave_type_id: int,
    data: schemas.LeaveTypeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = service.update_leave_type(
        db, leave_type_id, data, current_user
    )

    return APIResponse(
        code=200,
        message="Leave type updated successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.delete("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.soft_delete_leave_type(db, leave_type_id, current_user)

    return APIResponse(
        code=200,
        message="Leave type deleted successfully"
    )


# =====================================================
# LEAVE BALANCES
# =====================================================

@router.post("/balances", status_code=status.HTTP_201_CREATED)
def create_leave_balance(
    data: schemas.LeaveBalanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    balance = service.create_leave_balance(
        db, data, current_user
    )

    return APIResponse(
        code=201,
        message="Leave balance created successfully",
        data=schemas.LeaveBalanceResponse.model_validate(balance)
    )


# HR / SA / Manager Dashboard
@router.get("/balances", status_code=status.HTTP_200_OK)
def list_balances(
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    balances, total = service.get_all_balances(
        db, current_user, page, per_page, search, is_active
    )

    return APIResponse(
        code=200,
        message="Leave balances retrieved successfully",
        data={
            "items": [
                schemas.LeaveBalanceResponse.model_validate(b)
                for b in balances
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page)
        }
    )


# Single employee balances
@router.get("/balances/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee_balances(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    balances = service.get_employee_balances(
        db, employee_id, current_user
    )

    return APIResponse(
        code=200,
        message="Leave balances retrieved successfully",
        data=[
            schemas.LeaveBalanceResponse.model_validate(b)
            for b in balances
        ]
    )


# =====================================================
# LEAVE REQUESTS
# =====================================================

@router.post("/requests", status_code=status.HTTP_201_CREATED)
def create_leave_request(
    data: schemas.LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_request = service.create_leave_request(
        db, data, current_user
    )

    return APIResponse(
        code=201,
        message="Leave request created successfully",
        data=schemas.LeaveRequestResponse.model_validate(
            leave_request
        )
    )


@router.get("/requests", status_code=status.HTTP_200_OK)
def list_leave_requests(
    page: int = 1,
    per_page: int = 10,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    requests, total = service.get_leave_requests(
        db, current_user, page, per_page, is_active
    )

    return APIResponse(
        code=200,
        message="Leave requests retrieved successfully",
        data={
            "items": [
                schemas.LeaveRequestResponse.model_validate(r)
                for r in requests
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page)
        }
    )


@router.patch("/requests/{leave_id}", status_code=status.HTTP_200_OK)
def update_leave_request(
    leave_id: int,
    data: schemas.LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave = service.update_leave_request(
        db, leave_id, data, current_user
    )

    return APIResponse(
        code=200,
        message="Leave request updated successfully",
        data=schemas.LeaveRequestResponse.model_validate(leave)
    )


@router.delete("/requests/{leave_id}", status_code=status.HTTP_200_OK)
def delete_leave_request(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.soft_delete_leave_request(
        db, leave_id, current_user
    )

    return APIResponse(
        code=200,
        message="Leave request deleted successfully"
    )