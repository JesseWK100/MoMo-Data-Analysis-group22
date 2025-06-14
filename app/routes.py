from flask import Blueprint, jsonify, request
from app.utils import get_db_connection
import sqlite3
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

@main.route('/api/transactions')
def get_transactions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all transactions ordered by timestamp
        cursor.execute("""
            SELECT 
                id,
                timestamp,
                transaction_type,
                amount,
                description,
                recipient,
                sender,
                status
            FROM transactions 
            ORDER BY timestamp DESC
        """)
        
        transactions = []
        for row in cursor.fetchall():
            transaction = {
                'id': row[0],
                'timestamp': row[1],
                'transaction_type': row[2],
                'amount': row[3],
                'description': row[4],
                'recipient': row[5],
                'sender': row[6],
                'status': row[7]
            }
            transactions.append(transaction)
            
        conn.close()
        return jsonify(transactions)
        
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500 