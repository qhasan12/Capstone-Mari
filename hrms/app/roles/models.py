from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), unique=True, nullable=False)
    level = Column(Integer)
    description = Column(String(255))

    is_active = Column(Boolean, default=True, nullable=False)

    created_by = Column(Integer, ForeignKey("employees.id"), nullable=True)

    created_at = Column(DateTime(timezone=True),
    server_default=func.now(),   # 🔥 REQUIRED
    onupdate=func.now(),
    nullable=False
    )
    updated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),   # 🔥 REQUIRED
    onupdate=func.now(),
    nullable=False
    )

    employees = relationship(
    "Employee",
    back_populates="role",
    foreign_keys="Employee.role_id"   # 🔥 THIS IS REQUIRED
    )
    creator = relationship("Employee", foreign_keys=[created_by])