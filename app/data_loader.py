import sqlite3
from app.database import DB_NAME

def load_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "salary": row[3],
            "department": row[4],
            "contract_type": row[5],
            "work_hours": row[6]
        }
        for row in rows
    ]