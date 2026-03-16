from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(String(255))

    is_active = Column(Boolean, default=True)

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )
    

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"))

    role = relationship("Role", back_populates="permissions")
    permission = relationship(
    "Permission",
    back_populates="role_permissions"
    )