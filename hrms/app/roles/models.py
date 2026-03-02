from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    level = Column(Integer)  # optional: hierarchy level
    description = Column(String(255))

    employees = relationship("Employee", back_populates="role")