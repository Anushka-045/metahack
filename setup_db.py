import sqlite3

conn = sqlite3.connect("app/compliance.db")
cursor = conn.cursor()

# Delete old table
cursor.execute("DROP TABLE IF EXISTS employees")

# Create fresh correct table
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    salary INTEGER,
    department TEXT,
    contract_type TEXT,
    work_hours INTEGER
)
""")

conn.commit()
conn.close()

print("Fresh employees table created!")