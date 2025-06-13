from flask import Blueprint, jsonify, request, render_template, send_from_directory
from .models import get_db_connection
from .utils import format_transaction_row
from datetime import datetime, timedelta
import os

api = Blueprint('api', __name__)

@api.route('/')
def dashboard():
    return send_from_directory(os.path.dirname(__file__), 'dashboard.html')

@api.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get filter parameters
    date_from = request.args.get('dateFrom')
    date_to = request.args.get('dateTo')
    min_amount = request.args.get('amountThreshold')
    keyword = request.args.get('keyword')
    tx_type = request.args.get('type')

    query = """
        SELECT t.*, tt.name as type_name 
        FROM transactions t
        JOIN transaction_types tt ON t.tx_type_id = tt.id
        WHERE 1=1
    """
    params = []

    if date_from:
        query += " AND t.tx_timestamp >= ?"
        params.append(date_from)

    if date_to:
        query += " AND t.tx_timestamp <= ?"
        params.append(date_to)

    if min_amount:
        query += " AND t.amount >= ?"
        params.append(float(min_amount))

    if keyword:
        query += " AND (t.raw_body LIKE ? OR t.to_party LIKE ? OR t.from_party LIKE ?)"
        keyword_param = f"%{keyword}%"
        params.extend([keyword_param, keyword_param, keyword_param])

    if tx_type:
        query += " AND tt.name = ?"
        params.append(tx_type)

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    transactions = []
    for row in rows:
        tx = {
            'id': row['sms_id'],
            'type': row['type_name'],
            'amount': row['amount'],
            'date': row['tx_timestamp'],
            'receiver': row['to_party'] or row['from_party'],
            'raw_body': row['raw_body'],
            'direction': 'in' if row['amount'] > 0 else 'out'
        }
        transactions.append(tx)

    return jsonify(transactions)

@api.route('/api/types', methods=['GET'])
def get_transaction_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    types = cursor.execute('SELECT name FROM transaction_types ORDER BY name').fetchall()
    conn.close()
    
    return jsonify([row['name'] for row in types])

@api.route('/api/transactions/volume', methods=['GET'])
def get_transaction_volume():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT tt.name as type, COUNT(*) as count
        FROM transactions t
        JOIN transaction_types tt ON t.tx_type_id = tt.id
        WHERE 1=1
    '''
    params = []
    
    date_from = request.args.get('start_date')
    date_to = request.args.get('end_date')
    tx_type = request.args.get('type')
    
    if date_from:
        query += " AND t.tx_timestamp >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND t.tx_timestamp <= ?"
        params.append(date_to)
    
    if tx_type:
        query += " AND tt.name = ?"
        params.append(tx_type)
    
    query += " GROUP BY tt.name"
    
    results = cursor.execute(query, params).fetchall()
    conn.close()
    
    return jsonify({
        'labels': [row['type'] for row in results],
        'values': [row['count'] for row in results]
    })

@api.route('/api/transactions/monthly', methods=['GET'])
def get_monthly_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT strftime('%Y-%m', t.tx_timestamp) as month, COUNT(*) as count
        FROM transactions t
        JOIN transaction_types tt ON t.tx_type_id = tt.id
        WHERE 1=1
    '''
    params = []
    
    date_from = request.args.get('start_date')
    date_to = request.args.get('end_date')
    tx_type = request.args.get('type')
    
    if date_from:
        query += " AND t.tx_timestamp >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND t.tx_timestamp <= ?"
        params.append(date_to)
    
    if tx_type:
        query += " AND tt.name = ?"
        params.append(tx_type)
    
    query += " GROUP BY month ORDER BY month"
    
    results = cursor.execute(query, params).fetchall()
    conn.close()
    
    return jsonify({
        'labels': [row['month'] for row in results],
        'values': [row['count'] for row in results]
    })

@api.route('/api/transactions/distribution', methods=['GET'])
def get_transaction_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            CASE 
                WHEN t.amount > 0 THEN 'incoming'
                ELSE 'outgoing'
            END as direction,
            COUNT(*) as count
        FROM transactions t
        JOIN transaction_types tt ON t.tx_type_id = tt.id
        WHERE 1=1
    '''
    params = []
    
    date_from = request.args.get('start_date')
    date_to = request.args.get('end_date')
    tx_type = request.args.get('type')
    
    if date_from:
        query += " AND t.tx_timestamp >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND t.tx_timestamp <= ?"
        params.append(date_to)
    
    if tx_type:
        query += " AND tt.name = ?"
        params.append(tx_type)
    
    query += " GROUP BY direction"
    
    results = cursor.execute(query, params).fetchall()
    conn.close()
    
    incoming = next((row['count'] for row in results if row['direction'] == 'incoming'), 0)
    outgoing = next((row['count'] for row in results if row['direction'] == 'outgoing'), 0)
    
    return jsonify({
        'incoming': incoming,
        'outgoing': outgoing
    })

@api.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    summary = cursor.execute('''
        SELECT tt.name as type, COUNT(*) as count, SUM(t.amount) as total
        FROM transactions t
        JOIN transaction_types tt ON t.tx_type_id = tt.id
        GROUP BY tt.name
    ''').fetchall()
    conn.close()

    return jsonify({
        'types': [row['type'] for row in summary],
        'counts': [row['count'] for row in summary],
        'totals': [row['total'] for row in summary]
    })

