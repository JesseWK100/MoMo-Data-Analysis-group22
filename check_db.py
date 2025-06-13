import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('momo.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:", [table[0] for table in tables])
        
        if not tables:
            print("No tables found in the database!")
            return
            
        # Check transaction_types
        cursor.execute("SELECT * FROM transaction_types;")
        types = cursor.fetchall()
        print("\nTransaction Types:", [type[1] for type in types])
        
        # Check transactions
        cursor.execute("SELECT COUNT(*) FROM transactions;")
        count = cursor.fetchone()[0]
        print(f"\nTotal transactions: {count}")
        
        # Preview some transactions
        cursor.execute("""
            SELECT t.*, tt.name as type_name 
            FROM transactions t
            JOIN transaction_types tt ON t.tx_type_id = tt.id
            LIMIT 5
        """)
        rows = cursor.fetchall()
        print("\nSample transactions:")
        for row in rows:
            print(f"ID: {row['sms_id']}")
            print(f"Type: {row['type_name']}")
            print(f"Amount: {row['amount']}")
            print(f"Date: {row['tx_timestamp']}")
            print("---")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database()
