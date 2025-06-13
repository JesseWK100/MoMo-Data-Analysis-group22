import sqlite3

def create_db():
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            sms_id TEXT PRIMARY KEY,
            raw_body TEXT,
            tx_type_id INTEGER,
            amount INTEGER,
            currency TEXT,
            fee INTEGER,
            balance_after INTEGER,
            tx_timestamp TEXT,
            from_party TEXT,
            to_party TEXT,
            momo_tx_id TEXT,
            agent_id TEXT,
            extra_info TEXT,
            FOREIGN KEY(tx_type_id) REFERENCES transaction_types(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
