def handle_query(query, db, current_user):

    query_lower = query.lower()

    from app.agents.employee.tools import fetch_employees

    if "employee" in query_lower:
        data = fetch_employees(db, current_user)
        return {
            "message": "Employees fetched successfully",
            "data": data
        }

    return {"message": "Query not understood"}