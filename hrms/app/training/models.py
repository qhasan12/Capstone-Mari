from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import UniqueConstraint


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    training_title = Column(String(150))
    training_date = Column(Date)
    status = Column(String(50))
    
    is_active = Column(Boolean, default=True)

    employee = relationship("Employee", back_populates="training_records")
    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "training_title",
            "training_date",
            name="unique_employee_training"
        ),
    )