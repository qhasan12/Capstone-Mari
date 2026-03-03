from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    DateTime,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

<<<<<<< HEAD
    # is_HOD = Column(Boolean, default=False)
    # is_manager = Column(Boolean, default=False)

=======
>>>>>>> dev-branch
    full_name = Column(String(150), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    manager_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    salary = Column(
        Numeric(10, 2),
        nullable=True
    )

    joining_date = Column(Date, nullable=True)

    employment_status = Column(String(50), nullable=True)
    confirmation_status = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("salary >= 0", name="check_salary_positive"),
    )

    # Relationships
    department = relationship("Department", back_populates="employees")
    role = relationship(
    "Role",
    back_populates="employees",
    foreign_keys=[role_id]  # 🔥 THIS FIXES THE ERROR
    )
    manager = relationship(
        "Employee",
        remote_side=[id],
        backref="subordinates"
    )

    onboarding = relationship(
        "Onboarding",
        back_populates="employee",
        uselist=False
    )

    leave_balances = relationship(
        "LeaveBalance",
        back_populates="employee"
    )

    leave_requests = relationship(
        "LeaveRequest",
        back_populates="employee"
    )

    training_records = relationship(
        "TrainingRecord",
        back_populates="employee"
    )

    resignation = relationship(
        "Resignation",
        back_populates="employee",
        uselist=False
    )