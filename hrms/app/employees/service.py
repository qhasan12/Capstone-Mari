from psycopg2 import errors
from fastapi import HTTPException


# CREATE
def create_employee(db, data):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employees 
                (full_name, email, department_id, role_id, joining_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, full_name, email, department_id, role_id, joining_date
            """, (
                data.full_name,
                data.email,
                data.department_id,
                data.role_id,
                data.joining_date
            ))
            db.commit()
            return cursor.fetchone()
    except errors.UniqueViolation:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


# READ ALL
def get_employees(db):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT id, full_name, email, department_id, role_id, joining_date
            FROM employees
            ORDER BY id
        """)
        return cursor.fetchall()


# READ ONE
def get_employee_by_id(db, employee_id: int):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT id, full_name, email, department_id, role_id, joining_date
            FROM employees
            WHERE id = %s
        """, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        return employee


# UPDATE
def update_employee(db, employee_id: int, data):
    with db.cursor() as cursor:

        # Build dynamic update query
        fields = []
        values = []

        for key, value in data.dict(exclude_unset=True).items():
            fields.append(f"{key} = %s")
            values.append(value)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        values.append(employee_id)

        query = f"""
            UPDATE employees
            SET {', '.join(fields)}
            WHERE id = %s
            RETURNING id, full_name, email, department_id, role_id, joining_date
        """

        cursor.execute(query, tuple(values))
        db.commit()

        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Employee not found")

        return updated


# DELETE
def delete_employee(db, employee_id: int):
    with db.cursor() as cursor:
        cursor.execute("""
            DELETE FROM employees
            WHERE id = %s
            RETURNING id
        """, (employee_id,))
        db.commit()

        deleted = cursor.fetchone()

        if not deleted:
            raise HTTPException(status_code=404, detail="Employee not found")

        return {"message": "Employee deleted successfully"}