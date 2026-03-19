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

    full_name = Column(String(150), nullable=False)
    personal_email = Column(String(150), nullable=False, unique=True, index=True)

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
    invite_token = Column(String(255), nullable=True)
    invite_expiry = Column(DateTime, nullable=True)

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

    created_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    deleted_by = Column(Integer, ForeignKey("employees.id"), nullable=True)

    deleted_at = Column(DateTime, nullable=True, index=True)

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
        foreign_keys=[manager_id],
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

    training_assignments = relationship(
        "TrainingAssignment",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    resignation = relationship(
        "Resignation",
        back_populates="employee",
        uselist=False
    )
    auth_user = relationship(
        "AuthUser",
        back_populates="employee",
        uselist=False
    )
    # 🔥 Audit Relationships
    creator = relationship(
        "Employee",
        foreign_keys=[created_by],
        post_update=True
    )

    updater = relationship(
        "Employee",
        foreign_keys=[updated_by],
        post_update=True
    )

    deleter = relationship(
        "Employee",
        foreign_keys=[deleted_by],
        post_update=True
    )


