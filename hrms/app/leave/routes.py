from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.common.schemas import APIResponse
from . import service, schemas

router = APIRouter()

# =====================================================
# LEAVE TYPES (STANDARDIZED 5 OPERATIONS)
# =====================================================

@router.post("/types", status_code=status.HTTP_201_CREATED)
def create_leave_type(
    data: schemas.LeaveTypeCreate,
    db: Session = Depends(get_db)
):
    leave_type = service.create_leave_type(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Leave type created successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.get("/types", status_code=status.HTTP_200_OK)
def list_leave_types(db: Session = Depends(get_db)):
    leave_types = service.get_all_leave_types(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave types retrieved successfully",
        data=[
            schemas.LeaveTypeResponse.model_validate(lt)
            for lt in leave_types
        ]
    )


@router.get("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def get_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db)
):
    leave_type = service.get_leave_type_by_id(db, leave_type_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave type retrieved successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.patch("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def update_leave_type(
    leave_type_id: int,
    data: schemas.LeaveTypeUpdate,
    db: Session = Depends(get_db)
):
    leave_type = service.update_leave_type(db, leave_type_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave type updated successfully",
        data=schemas.LeaveTypeResponse.model_validate(leave_type)
    )


@router.delete("/types/{leave_type_id}", status_code=status.HTTP_200_OK)
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db)
):
    service.soft_delete_leave_type(db, leave_type_id)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave type deleted successfully"
    )


# =====================================================
# LEAVE BALANCES
# =====================================================

@router.post("/balances", status_code=status.HTTP_201_CREATED)
def create_leave_balance(
    data: schemas.LeaveBalanceCreate,
    db: Session = Depends(get_db)
):
    balance = service.create_leave_balance(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Leave balance created successfully",
        data=schemas.LeaveBalanceResponse.model_validate(balance)
    )


@router.get("/balances/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee_balances(
    employee_id: int,
    db: Session = Depends(get_db)
):
    balances = service.get_employee_balances(db, employee_id)

    return APIResponse(
        code=status.HTTP_200_OK,
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
    db: Session = Depends(get_db)
):
    leave_request = service.create_leave_request(db, data)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Leave request created successfully",
        data=schemas.LeaveRequestResponse.model_validate(leave_request)
    )


@router.get("/requests", status_code=status.HTTP_200_OK)
def list_leave_requests(db: Session = Depends(get_db)):
    requests = service.get_leave_requests(db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave requests retrieved successfully",
        data=[
            schemas.LeaveRequestResponse.model_validate(req)
            for req in requests
        ]
    )


@router.patch("/requests/{leave_id}", status_code=status.HTTP_200_OK)
def update_leave_request(
    leave_id: int,
    data: schemas.LeaveRequestUpdate,
    db: Session = Depends(get_db)
):
    leave = service.update_leave_request(db, leave_id, data)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Leave request updated successfully",
        data=schemas.LeaveRequestResponse.model_validate(leave)
    )