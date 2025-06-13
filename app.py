from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3

DB_FILE = "momo.db"

def get_db_connection():
    """Get database connection with row factory for dictionary returns."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return dictionaries instead of tuples
    return conn

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    @app.route("/")
    def dashboard():
        """Main dashboard page."""
        return render_template("dashboard.html")
    
    @app.route("/transactions", methods=["GET"])
    def get_transactions():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get optional filters from URL
        tx_type = request.args.get("type")
        min_amount = request.args.get("min_amount")
        max_amount = request.args.get("max_amount")
        
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        
        if tx_type:
            query += " AND transaction_type = ?"
            params.append(tx_type)
        if min_amount:
            query += " AND amount >= ?"
            params.append(float(min_amount))
        if max_amount:
            query += " AND amount <= ?"
            params.append(float(max_amount))
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in rows])
    
    @app.route("/transaction/<int:tx_id>", methods=["GET"])
    def get_transaction_by_id(tx_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify(dict(row))
        else:
            return jsonify({"error": "Transaction not found"}), 404
    
    @app.route("/summary", methods=["GET"])
    def get_summary():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total amount and count by type
        cursor.execute("""
            SELECT transaction_type, COUNT(*) as count, SUM(amount) as total
            FROM transactions
            GROUP BY transaction_type
        """)
        summary = cursor.fetchall()
        
        # Monthly summary
        cursor.execute("""
            SELECT
                strftime('%Y-%m', timestamp) as month,
                COUNT(*) as count,
                SUM(amount) as total
            FROM transactions
            GROUP BY month
            ORDER BY month ASC
        """)
        monthly = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "by_type": [dict(row) for row in summary],
            "monthly": [dict(row) for row in monthly]
        })
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "message": "MoMo API is running"})
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
