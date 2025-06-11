import sqlite3

def create_db():
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            receiver TEXT,
            amount INTEGER,
            date TEXT,
            raw_body TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
