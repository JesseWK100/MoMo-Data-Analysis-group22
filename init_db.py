import sqlite3
from datetime import datetime, timedelta
import random

def init_db():
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        recipient TEXT,
        sender TEXT,
        status TEXT NOT NULL
    )
    ''')
    
    # Sample transaction types
    transaction_types = ['send', 'receive', 'bill', 'airtime', 'merchant', 'savings']
    
    # Generate sample transactions
    for i in range(20):
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(10, 1000), 2)
        if transaction_type in ['send', 'bill', 'airtime', 'merchant']:
            amount = -amount
            
        timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        
        cursor.execute('''
        INSERT INTO transactions (timestamp, transaction_type, amount, description, recipient, sender, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            transaction_type,
            amount,
            f"Sample {transaction_type} transaction",
            "Recipient" if transaction_type == 'send' else None,
            "Sender" if transaction_type == 'receive' else None,
            "completed"
        ))
    
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db()
