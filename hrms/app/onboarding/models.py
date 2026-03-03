<<<<<<< HEAD
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Onboarding(Base):
    __tablename__ = "onboarding"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)

    appointment_letter_generated = Column(Boolean, default=False)
    email_created = Column(Boolean, default=False)
    resources_allocated = Column(Boolean, default=False)
    orientation_sent = Column(Boolean, default=False)

    stage = Column(String(50))
    is_active = Column(Boolean, default=True)

    employee = relationship("Employee", back_populates="onboarding")
=======
>>>>>>> dev-branch
