import sqlite3

def insert_transactions(transactions):
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()

    for tx in transactions:
        cursor.execute('''
            INSERT INTO transactions (type, receiver, amount, date, raw_body)
            VALUES (?, ?, ?, ?, ?)
        ''', (tx.get("type"), tx.get("receiver"), tx.get("amount"), tx.get("date"), tx.get("raw_body")))

    conn.commit()
    conn.close()

