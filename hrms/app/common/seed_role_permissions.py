from sqlalchemy.orm import Session
from app.roles.models import Role, RolePermission
from app.permissions.models import Permission


ROLE_PERMISSION_MAP = {
    # SuperAdmin gets everything
    "SA": "*",
    # HR permissions
    "HR": [
        "employee:create",
        "employee:view",
        "employee:update",
        "employee:delete",
        "department:view",
        "department:update",
        "hiring_request:create",
        "hiring_request:view",
        "leave_request:view",
        "leave_request:approve",
        "training:create",
        "training:view",
        "resignation:view",
        "resignation:approve",
    ],
    # Manager permissions
    "MGR": [
        "employee:view_team",
        "leave_request:view_team",
        "leave_request:approve",
        "resignation:view_team",
    ],
    # Employee permissions
    "EMP": [
        "employee:view_self",
        "employee:update",
        "leave_request:create",
        "leave_request:view_self",
        "leave_request:update",
        "resignation:create",
        "resignation:view_self",
    ],
}


def seed_role_permissions(db: Session):

    roles = db.query(Role).all()
    permissions = db.query(Permission).all()

    perm_map = {p.name: p.id for p in permissions}

    for role in roles:

        role_perms = ROLE_PERMISSION_MAP.get(role.title)

        if role_perms is None:
            continue

        if role_perms == "*":
            role_perms = perm_map.keys()

        for perm_name in role_perms:

            perm_id = perm_map.get(perm_name)

            exists = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == perm_id,
                )
                .first()
            )

            if not exists:
                db.add(RolePermission(role_id=role.id, permission_id=perm_id))

    db.commit()
