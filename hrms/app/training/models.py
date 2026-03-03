from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    training_title = Column(String(150))
    training_date = Column(Date)
    status = Column(String(50))

    employee = relationship("Employee", back_populates="training_records")