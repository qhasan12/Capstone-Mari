from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

<<<<<<< HEAD
=======
from sqlalchemy.sql import func

>>>>>>> 34d15635a6fceed9808c50c67a2e80bdb3a82ea3

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
<<<<<<< HEAD
    created_at = Column(DateTime, default=datetime.utcnow)
=======
    created_at = Column(DateTime, server_default=func.now())
>>>>>>> 34d15635a6fceed9808c50c67a2e80bdb3a82ea3

    employees = relationship("Employee", back_populates="department")
    hiring_requests = relationship("HiringRequest", back_populates="department")