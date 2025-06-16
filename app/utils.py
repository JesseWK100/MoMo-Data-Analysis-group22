import sqlite3
import os
from pathlib import Path

def get_db_connection():
    try:
        # Get the absolute path to the database file
        db_path = Path(__file__).parent.parent / 'momo.db'
        
        # Check if database file exists
        if not db_path.exists():
            raise FileNotFoundError(f"Database file not found at {db_path}")
            
        # Connect to the database
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        
        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise 