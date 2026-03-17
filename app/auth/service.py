import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from app.auth.models import AuthUser, AuthToken
from app.employees.models import Employee
from app.auth.security import create_access_token
from app.core.email import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# PASSWORD HELPERS
# =========================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


# =========================
# REGISTER CREDENTIALS
# =========================

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.auth.models import AuthUser
from app.auth.service import hash_password
from app.employees.models import Employee
from app.leave.models import LeaveType, LeaveBalance


def register_user(db: Session, token: str, password: str):

    employee = db.query(Employee).filter(
        Employee.invite_token == token
    ).first()

    if not employee:
        raise HTTPException(400, "Invalid invitation token")

    if employee.invite_expiry < datetime.utcnow():
        raise HTTPException(400, "Invitation expired")

    existing = db.query(AuthUser).filter(
        AuthUser.employee_id == employee.id
    ).first()

    if existing:
        raise HTTPException(400, "Account already exists")

    # Create auth user
    user = AuthUser(
        email=employee.email,
        employee_id=employee.id,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.flush()  # get user without committing yet

    # =========================
    # Allocate Leave Balances
    # =========================
    leave_types = db.query(LeaveType).filter(
        LeaveType.is_active == True
    ).all()

    for lt in leave_types:

        existing_balance = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee.id,
            LeaveBalance.leave_type_id == lt.id
        ).first()

        if not existing_balance:

            balance = LeaveBalance(
                employee_id=employee.id,
                leave_type_id=lt.id,
                total_leaves=lt.default_allocation,
                used_leaves=0,
                remaining_leaves=lt.default_allocation,
                is_active=True
            )

            db.add(balance)

    # remove token after use
    employee.invite_token = None
    employee.invite_expiry = None

    db.commit()
    db.refresh(user)

    return user


# =========================
# LOGIN
# =========================
def login_user(db: Session, email: str, password: str):
    db.query(AuthToken).filter(AuthToken.expires_at < datetime.now(timezone.utc)).delete()
    db.commit()
    
    existing_token = db.query(AuthToken).filter(
        AuthToken.user_id == user.id,
        AuthToken.expires_at > datetime.now(timezone.utc)
    ).first()
    if existing_token:
        raise HTTPException(400, "User already logged in")

    user = db.query(AuthUser).filter(AuthUser.email == email).first()




    if not user:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_active:
        raise HTTPException(403, "Account disabled")

    # remove expired tokens


    token, expiry = create_access_token({
        "user_id": user.id,
        "employee_id": user.employee_id
    })

    db_token = AuthToken(
        user_id=user.id,
        token=token,
        expires_at=expiry
    )

    db.add(db_token)
    db.commit()

    return token

# =========================
# CHANGE PASSWORD
# =========================

def change_password(
    db: Session,
    user: AuthUser,
    old_password: str,
    new_password: str
):

    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    if new_password == old_password:
        raise HTTPException(status_code=400, detail="New password cannot be same as old password")

    user.password_hash = hash_password(new_password)

    db.commit()

    return True


# =========================
# SEND OTP
# =========================

def send_otp(db: Session, email: str):

    user = db.query(AuthUser).filter(AuthUser.email == email).first()
    

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.otp_verified = False
    if user.otp_expiry and user.otp_expiry > datetime.utcnow():
        raise HTTPException(400, "OTP already sent. Please wait.")

    otp = str(random.randint(100000, 999999))

    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)

    db.commit()

    send_email(
        email,
        "HRMS Password Reset OTP",
        f"Your OTP for password reset is: {otp}\n\nThis OTP will expire in 10 minutes."
    )

    return True


# =========================
# VERIFY OTP
# =========================

def verify_otp(db: Session, email: str, otp: str):

    user = db.query(AuthUser).filter(AuthUser.email == email).first()

    if not user or user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if not user.otp_expiry or user.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")
    user.otp_verified = True
    db.commit()
    return True


# =========================
# RESET PASSWORD
# =========================

def reset_password(db: Session, email: str, new_password: str):

    user = db.query(AuthUser).filter(AuthUser.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    if not user.otp_verified:
        raise HTTPException(status_code=400, detail="OTP verification required")

    # check if new password equals old password
    if verify_password(new_password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="New password cannot be same as old password"
        )

    # update password
    user.password_hash = hash_password(new_password)

    user.otp_code = None
    user.otp_expiry = None
    user.otp_verified = False

    db.commit()

    return True

def logout_user(db: Session, token: str):

    token_record = db.query(AuthToken).filter(
        AuthToken.token == token
    ).first()

    if token_record:
        db.delete(token_record)
        db.commit()


    return True