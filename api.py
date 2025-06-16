from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("your_database.db")  # Replace with actual DB name
    conn.row_factory = sqlite3.Row  # Allows access by column name
    return conn

# Route to get transaction summary
@app.route("/api/summary", methods=["GET"])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate total balance
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type = 'receive' THEN amount ELSE 0 END) -
            SUM(CASE WHEN transaction_type = 'send' THEN amount ELSE 0 END) AS total_balance
        FROM transactions
    """)
    result = cursor.fetchone()
    total_balance = result["total_balance"] if result["total_balance"] is not None else 0

    # Count transactions by type
    cursor.execute("""
        SELECT transaction_type, COUNT(*) as count
        FROM transactions
        GROUP BY transaction_type
    """)
    type_counts = [dict(row) for row in cursor.fetchall()]

    # Get 5 most recent transactions
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

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

