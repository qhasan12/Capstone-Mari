from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Date,
    DateTime,
    Boolean,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import UniqueConstraint

class HiringRequest(Base):
    __tablename__ = "hiring_requests"

    id = Column(Integer, primary_key=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    role_title = Column(String(100), nullable=False)
    required_skills = Column(Text, nullable=False)

    experience_level = Column(String(50), nullable=True)
    budget_range = Column(String(50), nullable=True)

    status = Column(String(50), default="Draft", nullable=False)
    approval_status = Column(String(50), default="Pending", nullable=False)

    jd_text = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    department = relationship(
        "Department",
        back_populates="hiring_requests"
    )

    job_postings = relationship(
        "JobPosting",
        back_populates="hiring_request",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "role_title",
            "is_active",
            name="uq_active_hiring_request_per_role_department"
        ),
    )

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)

    hiring_request_id = Column(
        Integer,
        ForeignKey("hiring_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    posted_date = Column(Date, nullable=True)
    closing_date = Column(Date, nullable=True)

    status = Column(String(50), default="Open", nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    hiring_request = relationship(
        "HiringRequest",
        back_populates="job_postings"
    )
    __table_args__ = (
    UniqueConstraint(
        "hiring_request_id",
        "is_active",
        name="uq_active_job_posting_per_hiring_request"
    ),
    )   