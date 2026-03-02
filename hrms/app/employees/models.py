from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    is_HOD = Column(Boolean, default=False)
    is_manager = Column(Boolean, default=False)

    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="employees")
    salary = Column(Numeric(10, 2))
    joining_date = Column(Date)

    employment_status = Column(String(50))
    confirmation_status = Column(String(50))

    department = relationship("Department", back_populates="employees")
    manager = relationship("Employee", remote_side=[id])

    onboarding = relationship("Onboarding", back_populates="employee", uselist=False)
    leave_balances = relationship("LeaveBalance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    training_records = relationship("TrainingRecord", back_populates="employee")
    resignation = relationship("Resignation", back_populates="employee", uselist=False)