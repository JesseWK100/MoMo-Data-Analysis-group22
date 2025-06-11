#!/usr/bin/env python3
import sqlite3, json
from extract_process import extract_all

DB_FILE = 'momo.db'
XML_FILE = 'modified_sms_v2.xml'
TYPE_LIST = ['incoming','payment','transfer','deposit',
             'airtime','cash_power','withdrawal','otp']

def ensure_types(cur):
    for t in TYPE_LIST:
        cur.execute("INSERT OR IGNORE INTO transaction_types(name) VALUES(?)", (t,))

def populate():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    ensure_types(cur)
    conn.commit()

    recs = extract_all(XML_FILE)
    for r in recs:
        # get type_id
        cur.execute("SELECT id FROM transaction_types WHERE name=?", (r['tx_type'],))
        type_id = cur.fetchone()[0]
        # insert
        cur.execute("""
        INSERT OR IGNORE INTO transactions
        (sms_id, raw_body, tx_type_id, amount, currency, fee,
         balance_after, tx_timestamp, from_party, to_party,
         momo_tx_id, agent_id, extra_info)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            r['sms_id'], r['raw_body'], type_id, r.get('amount',0), r['currency'],
            r.get('fee',0), r.get('balance_after'),
            r['tx_timestamp'], r.get('from_party'),
            r.get('to_party'), r.get('momo_tx_id'),
            r.get('agent_id'), r.get('extra_info')
        ))
    conn.commit()
    print(f"Inserted {len(recs)} transactions into {DB_FILE}")
    conn.close()

if __name__ == '__main__':
    populate()
