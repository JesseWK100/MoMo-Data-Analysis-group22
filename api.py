@app.route("/api/summary", methods=["GET"])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total balance (receive adds, send subtracts)
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type = 'receive' THEN amount ELSE 0 END) -
            SUM(CASE WHEN transaction_type = 'send' THEN amount ELSE 0 END) AS total_balance
    FROM transactions
    """)
    total_balance = cursor.fetchone()["total_balance"] or 0

    # Transaction counts per type
    cursor.execute("""
        SELECT transaction_type, COUNT(*) as count
        FROM transactions
        GROUP BY transaction_type
    """)
    type_counts = [dict(row) for row in cursor.fetchall()]

    # Get recent transactions (optional)
    cursor.execute("""
        SELECT id, transaction_type, amount, timestamp, description
        FROM transactions
        ORDER BY timestamp DESC
        LIMIT 5
    """)
    recent_transactions = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        "total_balance": total_balance,
        "type_counts": type_counts,
        "recent_transactions": recent_transactions
    })
