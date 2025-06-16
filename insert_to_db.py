import sqlite3

# Optional: print to confirm the script is running
print("Script started running...")

# Create a database file called momo.db (or connect if it exists)
conn = sqlite3.connect("momo.db")
cursor = conn.cursor()

# Create the transactions table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount INTEGER,
        sender TEXT,
        receiver TEXT,
        date TEXT,
        raw_message TEXT
    )
''')

# Optional: insert dummy data for testing
cursor.execute('''
    INSERT INTO transactions (type, amount, sender, receiver, date, raw_message)
    VALUES (?, ?, ?, ?, ?, ?)
''', ("Incoming Money", 5000, "John Doe", "You", "2024-01-01 10:00:00", "You have received 5000 RWF from John Doe."))

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and data inserted.")
