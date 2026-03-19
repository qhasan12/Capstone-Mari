from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import UniqueConstraint


class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)

    title = Column(String(150), nullable=False)
    description = Column(String(500))
    training_date = Column(Date, nullable=False)

    created_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    deleted_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True, index=True)

    is_active = Column(Boolean, default=True)

    # ✅ Correct relationship
    assignments = relationship(
        "TrainingAssignment",
        back_populates="training",
        cascade="all, delete-orphan"
    )


class TrainingAssignment(Base):
    __tablename__ = "training_assignments"

    id = Column(Integer, primary_key=True)

    training_id = Column(Integer, ForeignKey("trainings.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))

    status = Column(String(50), default="Assigned")

    # ✅ Correct
    training = relationship(
        "Training",
        back_populates="assignments"
    )

    # ✅ IMPORTANT FIX (disambiguation happens here)
    employee = relationship(
        "Employee",
        back_populates="training_assignments",
        foreign_keys=[employee_id]
    )

    created_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    deleted_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True, index=True)

    __table_args__ = (
        UniqueConstraint(
            "training_id",
            "employee_id",
            name="unique_training_employee"
        ),
    )