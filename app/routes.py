from flask import Blueprint, jsonify, request
from .models import get_db_connection
from .utils import format_transaction_row

api = Blueprint('api', __name__)

@api.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()

    tx_type = request.args.get('type')
    date_from = request.args.get('from')
    date_to = request.args.get('to')

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if tx_type:
        query += " AND type = ?"
        params.append(tx_type)

    if date_from:
        query += " AND date >= ?"
        params.append(date_from)

    if date_to:
        query += " AND date <= ?"
        params.append(date_to)

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    return jsonify([format_transaction_row(row) for row in rows])

@api.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    summary = cursor.execute('''
        SELECT type, COUNT(*) as count, SUM(amount) as total
        FROM transactions
        GROUP BY type
    ''').fetchall()
    conn.close()

    return jsonify([{ "type": row["type"], "count": row["count"], "total": row["total"] } for row in summary])

