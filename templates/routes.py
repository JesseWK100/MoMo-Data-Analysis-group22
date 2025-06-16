from flask import Blueprint, jsonify, request
from templates.utils import get_transactions
from datetime import datetime
import json
from pathlib import Path

main = Blueprint('main', __name__)

@main.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

@main.route('/api/transactions')
def get_transactions_route():
    try:
        # Get all transactions
        transactions = get_transactions()
        
        # Apply filters if provided
        search = request.args.get('search', '').lower()
        type_filter = request.args.get('type')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        filtered_transactions = []
        for txn in transactions:
            # Apply search filter
            if search and search not in txn.get('raw_body', '').lower():
                continue
                
            # Apply type filter
            if type_filter and txn.get('tx_type') != type_filter:
                continue
                
            # Apply date filters
            if date_from and txn.get('tx_timestamp', '') < date_from:
                continue
            if date_to and txn.get('tx_timestamp', '') > date_to:
                continue
                
            filtered_transactions.append(txn)
            
        return jsonify(filtered_transactions)
        
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"error": str(e)}), 500

@main.route('/api/transactions/<transaction_type>', methods=['GET'])
def get_transactions_by_type(transaction_type):
    try:
        # Get all transactions
        transactions = get_transactions()
        
        # Filter by type
        filtered_transactions = [
            txn for txn in transactions 
            if txn.get('tx_type') == transaction_type
        ]
        
        return jsonify(filtered_transactions)
        
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"error": str(e)}), 500

@main.route('/api/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['transaction_type', 'amount', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Get existing transactions
        transactions = get_transactions()
        
        # Create new transaction
        new_transaction = {
            'sms_id': f"0|M-Money|{int(datetime.now().timestamp() * 1000)}",
            'raw_body': data.get('description', ''),
            'tx_type': data['transaction_type'],
            'tx_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'currency': 'RWF',
            'amount': float(data['amount']),
            'from_party': data.get('sender'),
            'to_party': data.get('recipient')
        }
        
        # Add to transactions list
        transactions.append(new_transaction)
        
        # Save back to file
        json_path = Path(__file__).parent / 'transactions.json'
        with open(json_path, 'w') as f:
            json.dump(transactions, f, indent=2)
        
        return jsonify({
            "message": "Transaction created successfully",
            "transaction": new_transaction
        }), 201
        
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return jsonify({"error": str(e)}), 500 