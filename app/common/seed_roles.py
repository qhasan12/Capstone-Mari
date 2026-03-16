from sqlalchemy.orm import Session
from app.roles.models import Role

DEFAULT_ROLES = [
    {"title": "SA", "level": 1, "description": "SuperAdmin"},
    {"title": "HR", "level": 2, "description": "Human Resources"},
    {"title": "MGR", "level": 3, "description": "Manager"},
    {"title": "EMP", "level": 4, "description": "Employee"},
]


def seed_roles(db: Session):

    for role_data in DEFAULT_ROLES:

        existing_role = db.query(Role).filter(
            Role.title == role_data["title"]
        ).first()

        if not existing_role:
            role = Role(**role_data)
            db.add(role)

    db.commit()