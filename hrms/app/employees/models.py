from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    joining_date = Column(Date, nullable=True)