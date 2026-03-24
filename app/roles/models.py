from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), unique=True, nullable=False)
    level = Column(Integer)
    description = Column(String(255))

    is_active = Column(Boolean, default=True, nullable=False)

    # ✅ AUDIT FIELDS (CONSISTENT WITH YOUR SYSTEM)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=True)

    updated_at = Column(DateTime(timezone=True), nullable=True)
    updated_by = Column(Integer, nullable=True)

    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)

    # ✅ RELATIONSHIPS
    employees = relationship(
        "Employee",
        back_populates="role",
        foreign_keys="Employee.role_id"
    )

    permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan"
    )