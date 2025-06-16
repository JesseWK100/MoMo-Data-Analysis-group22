import sqlite3
from datetime import datetime, timedelta
import random

def init_db():
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    # Create transaction_types table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaction_types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sms_id TEXT UNIQUE NOT NULL,
        raw_body TEXT NOT NULL,
        tx_type_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        currency TEXT NOT NULL,
        fee INTEGER DEFAULT 0,
        balance_after INTEGER,
        tx_timestamp DATETIME NOT NULL,
        from_party TEXT,
        to_party TEXT,
        momo_tx_id TEXT,
        agent_id TEXT,
        extra_info TEXT,
        FOREIGN KEY (tx_type_id) REFERENCES transaction_types(id)
    )
    ''')
    
    # Insert transaction types
    transaction_types = [
        (1, 'incoming'),
        (2, 'payment'),
        (3, 'transfer'),
        (4, 'deposit'),
        (5, 'airtime'),
        (6, 'cash_power'),
        (7, 'withdrawal'),
        (8, 'otp')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO transaction_types (id, name) VALUES (?, ?)', transaction_types)
    
    # Generate sample transactions
    for i in range(20):
        tx_type_id = random.randint(1, 8)
        amount = random.randint(1000, 100000)
        timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        sms_id = f"0|M-Money|{int(datetime.now().timestamp() * 1000)}"
        
        cursor.execute('''
        INSERT INTO transactions (
            sms_id, raw_body, tx_type_id, amount, currency, fee, 
            tx_timestamp, from_party, to_party, momo_tx_id, agent_id, extra_info
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sms_id,
            f"Sample transaction {i}",
            tx_type_id,
            amount,
            'RWF',
            0,
            timestamp,
            "Sender" if tx_type_id in [1, 4] else None,
            "Recipient" if tx_type_id in [2, 3, 5, 6] else None,
            f"TX{i}",
            None,
            None
        ))
    
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db()
