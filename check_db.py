import sqlite3

conn = sqlite3.connect('momo.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in the database:", cursor.fetchall())

# Preview records (limit to 5)
cursor.execute("SELECT * FROM transactions LIMIT 5;")
rows = cursor.fetchall()
print("Sample records:", rows)

conn.close()
