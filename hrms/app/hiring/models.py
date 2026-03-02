from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class HiringRequest(Base):
    __tablename__ = "hiring_requests"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))

    role_title = Column(String(100))
    required_skills = Column(Text)
    experience_level = Column(String(50))
    budget_range = Column(String(50))
    status = Column(String(50))
    jd_text = Column(Text)
    approval_status = Column(String(50))

    department = relationship("Department", back_populates="hiring_requests")
    job_postings = relationship("JobPosting", back_populates="hiring_request")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True)
    hiring_request_id = Column(Integer, ForeignKey("hiring_requests.id"))

    posted_date = Column(Date)
    closing_date = Column(Date)
    status = Column(String(50))

    hiring_request = relationship("HiringRequest", back_populates="job_postings")