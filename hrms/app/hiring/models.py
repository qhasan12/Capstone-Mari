from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class HiringRequest(Base):
    __tablename__ = "hiring_requests"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    role_title = Column(String(100), nullable=False)
    required_skills = Column(Text, nullable=False)
    experience_level = Column(String(50))
    budget_range = Column(String(50))
    status = Column(String(50), default="Draft")
    jd_text = Column(Text)
    approval_status = Column(String(50), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = relationship("Department", back_populates="hiring_requests")
    job_postings = relationship(
        "JobPosting",
        back_populates="hiring_request",
        cascade="all, delete-orphan"
    )


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True)
    hiring_request_id = Column(
        Integer,
        ForeignKey("hiring_requests.id"),
        nullable=False
    )

    posted_date = Column(Date)
    closing_date = Column(Date)
    status = Column(String(50), default="Open")

    created_at = Column(DateTime, default=datetime.utcnow)

    hiring_request = relationship("HiringRequest", back_populates="job_postings")