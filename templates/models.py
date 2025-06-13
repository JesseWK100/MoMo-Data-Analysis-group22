import sqlite3

def get_db_connection():
    conn = sqlite3.connect('momo.db')
    conn.row_factory = sqlite3.Row  # returns dictionaries instead of tuples
    return conn

