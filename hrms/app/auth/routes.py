from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.common.schemas import APIResponse

from . import service, schemas
from app.auth.security import get_current_user


router = APIRouter()
# =========================
# REGISTER
# =========================

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: schemas.RegisterRequest, db: Session = Depends(get_db)):

    user = service.register_user(db, data.employee_id, data.password)

    return APIResponse(
        code=201,
        message="Credentials created successfully",
        data=schemas.AuthUserResponse.model_validate(user)
    )


# =========================
# LOGIN
# =========================

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = service.login_user(db, form_data.username, form_data.password)

    return APIResponse(
        code=200,
        message="Login successful",
        data={"access_token": user, "token_type": "bearer"}
    )

# =========================
# CHANGE PASSWORD
# =========================

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    data: schemas.ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service.change_password(
        db,
        current_user,
        data.old_password,
        data.new_password
    )

    return APIResponse(
        code=200,
        message="Password changed successfully",
        data=None
    )


# =========================
# FORGOT PASSWORD
# =========================

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(
    data: schemas.ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    service.send_otp(db, data.email)

    return APIResponse(
        code=200,
        message="OTP sent successfully",
        data=None
    )


# =========================
# VERIFY OTP
# =========================

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(
    data: schemas.VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    service.verify_otp(db, data.email, data.otp)

    return APIResponse(
        code=200,
        message="OTP verified successfully",
        data=None
    )


# =========================
# RESET PASSWORD
# =========================

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    data: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    service.reset_password(db, data.email, data.new_password)

    return APIResponse(
        code=200,
        message="Password reset successfully",
        data=None
    )