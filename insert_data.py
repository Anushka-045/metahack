import sqlite3

conn = sqlite3.connect("app/compliance.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO employees (id, name, age, salary, department, contract_type, work_hours)
VALUES
(1, 'Alice', 16, 3000, 'HR', 'full-time', 40),
(2, 'Bob', 25, 5000, 'IT', 'full-time', 40),
(3, 'Charlie', 17, 2000, 'Finance', 'intern', 20)
""")

conn.commit()
conn.close()

print("Data inserted!")