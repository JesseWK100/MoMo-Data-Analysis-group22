import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('momo.db')
        cursor = conn.cursor()
        
        # Check if transactions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        if cursor.fetchone() is None:
            print("Transactions table does not exist!")
            return
        
        # Get total number of transactions
        cursor.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        print(f"Total number of transactions: {count}")
        
        # Get sample of transactions
        cursor.execute("SELECT * FROM transactions LIMIT 5")
        rows = cursor.fetchall()
        print("\nSample transactions:")
        for row in rows:
            print(row)
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database()
