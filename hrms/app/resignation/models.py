<<<<<<< HEAD
from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    resignation_date = Column(Date)
    notice_end_date = Column(Date)
    manager_approved = Column(Boolean, default=False)
    status = Column(String(50))

    is_active = Column(Boolean, default=True)

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

    resignation = relationship("Resignation", back_populates="clearance")
=======
>>>>>>> dev-branch
