from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AuthUser(Base):
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(150), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    otp_code = Column(String(6), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    otp_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="auth_user")
    
    
class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("auth_users.id", ondelete="CASCADE"))

    token = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("AuthUser")