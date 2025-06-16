from flask import Blueprint, jsonify, request
from app.utils import get_db_connection
import sqlite3
from datetime import datetime

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
                sms_id,
                raw_body,
                tx_type_id,
                amount,
                currency,
                fee,
                tx_timestamp,
                from_party,
                to_party,
                momo_tx_id,
                agent_id,
                extra_info
            FROM transactions 
            ORDER BY tx_timestamp DESC
            LIMIT 100
        """)
        
        transactions = []
        for row in cursor.fetchall():
            try:
                transaction = {
                    'id': row[0],  # Using sms_id as the unique identifier
                    'message': row[1],
                    'transaction_type': str(row[2]),
                    'amount': float(row[3]),
                    'currency': row[4],
                    'fee': float(row[5]) if row[5] is not None else 0,
                    'timestamp': row[6],
                    'sender': row[7],
                    'recipient': row[8],
                    'transaction_id': row[9],
                    'agent_id': row[10],
                    'extra_info': row[11]
                }
                transactions.append(transaction)
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
            
        conn.close()
        return jsonify(transactions)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@main.route('/api/transactions/<transaction_type>', methods=['GET'])
def get_transactions_by_type(transaction_type):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get transactions of specific type
        cursor.execute("""
            SELECT 
                sms_id,
                raw_body,
                tx_type_id,
                amount,
                currency,
                fee,
                tx_timestamp,
                from_party,
                to_party,
                momo_tx_id,
                agent_id,
                extra_info
            FROM transactions 
            WHERE tx_type_id = ?
            ORDER BY tx_timestamp DESC
            LIMIT 100
        """, (transaction_type,))
        
        transactions = []
        for row in cursor.fetchall():
            try:
                transaction = {
                    'id': row[0],  # Using sms_id as the unique identifier
                    'message': row[1],
                    'transaction_type': str(row[2]),
                    'amount': float(row[3]),
                    'currency': row[4],
                    'fee': float(row[5]) if row[5] is not None else 0,
                    'timestamp': row[6],
                    'sender': row[7],
                    'recipient': row[8],
                    'transaction_id': row[9],
                    'agent_id': row[10],
                    'extra_info': row[11]
                }
                transactions.append(transaction)
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
            
        conn.close()
        return jsonify(transactions)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@main.route('/api/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['transaction_type', 'amount', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new transaction
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (
                timestamp,
                transaction_type,
                amount,
                description,
                recipient,
                sender,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            data['transaction_type'],
            data['amount'],
            data['description'],
            data.get('recipient'),
            data.get('sender'),
            'completed'
        ))
        
        conn.commit()
        transaction_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "message": "Transaction created successfully",
            "transaction_id": transaction_id
        }), 201
        
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500 