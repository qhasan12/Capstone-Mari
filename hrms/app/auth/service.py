import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from app.auth.models import AuthUser
from app.employees.models import Employee
from app.auth.security import create_access_token
from app.core.email import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# PASSWORD HELPERS
# =========================

def hash_password(password: str):
    password = password[:72]   # bcrypt limit
    return pwd_context.hash(password)

def verify_password(password, hashed):
    password = password[:72]   # bcrypt limit
    return pwd_context.verify(password, hashed)


# =========================
# REGISTER CREDENTIALS
# =========================

def register_user(db: Session, employee_id: int, password: str):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(AuthUser).filter(
        AuthUser.employee_id == employee_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Account already exists")

    user = AuthUser(
        email=employee.email,
        employee_id=employee_id,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================
# LOGIN
# =========================

def login_user(db: Session, email: str, password: str):

    user = db.query(AuthUser).filter(AuthUser.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {
            "user_id": user.id,
            "employee_id": user.employee_id
        }
    )

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

    if user.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    return True


# =========================
# RESET PASSWORD
# =========================

def reset_password(db: Session, email: str, new_password: str):

    user = db.query(AuthUser).filter(AuthUser.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(new_password)

    user.otp_code = None
    user.otp_expiry = None

    db.commit()

    return True