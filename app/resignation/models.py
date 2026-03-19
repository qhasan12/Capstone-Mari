from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.sql import func


class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    resignation_date = Column(Date)
    notice_end_date = Column(Date)
    manager_approved = Column(Boolean, default=False)
    status = Column(String(50))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)

    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)

    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(Integer, nullable=True)

    employee = relationship("Employee", back_populates="resignation")
    clearance = relationship("ClearanceRecord", back_populates="resignation", uselist=False)


class ClearanceRecord(Base):
    __tablename__ = "clearance_records"

    id = Column(Integer, primary_key=True)
    resignation_id = Column(Integer, ForeignKey("resignations.id"), unique=True)

    laptop_returned = Column(Boolean, default=False)
    access_revoked = Column(Boolean, default=False)
    email_deactivated = Column(Boolean, default=False)
    clearance_completed = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, nullable=True)

    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)

    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(Integer, nullable=True)

    resignation = relationship("Resignation", back_populates="clearance")
