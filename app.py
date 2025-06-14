from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

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
    def index():
        """Main index page."""
        return render_template("index.html")
    
    @app.route("/api/transactions", methods=["GET"])
    def get_transactions():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get optional filters from URL
        tx_type = request.args.get("type")
        min_amount = request.args.get("min_amount")
        max_amount = request.args.get("max_amount")
        date_from = request.args.get("dateFrom")
        date_to = request.args.get("dateTo")
        
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
        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from)
        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in rows])
    
    @app.route("/api/transactions/volume", methods=["GET"])
    def get_transaction_volume():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get date range from request
        date_from = request.args.get("start_date")
        date_to = request.args.get("end_date")
        tx_type = request.args.get("type")
        
        query = """
            SELECT 
                strftime('%Y-%m-%d', timestamp) as date,
                COUNT(*) as count,
                SUM(amount) as total
            FROM transactions
            WHERE 1=1
        """
        params = []
        
        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from)
        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to)
        if tx_type:
            query += " AND transaction_type = ?"
            params.append(tx_type)
            
        query += " GROUP BY date ORDER BY date"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in rows])
    
    @app.route("/api/transactions/distribution", methods=["GET"])
    def get_transaction_distribution():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get date range from request
        date_from = request.args.get("start_date")
        date_to = request.args.get("end_date")
        tx_type = request.args.get("type")
        
        query = """
            SELECT 
                transaction_type,
                COUNT(*) as count,
                SUM(amount) as total
            FROM transactions
            WHERE 1=1
        """
        params = []
        
        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from)
        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to)
        if tx_type:
            query += " AND transaction_type = ?"
            params.append(tx_type)
            
        query += " GROUP BY transaction_type"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in rows])
    
    @app.route("/api/summary", methods=["GET"])
    def get_summary():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total balance
        cursor.execute("SELECT SUM(amount) as total FROM transactions")
        total_balance = cursor.fetchone()["total"] or 0
        
        # Get transaction counts by type
        cursor.execute("""
            SELECT transaction_type, COUNT(*) as count
            FROM transactions
            GROUP BY transaction_type
        """)
        type_counts = [dict(row) for row in cursor.fetchall()]
        
        # Get recent transactions
        cursor.execute("""
            SELECT * FROM transactions
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
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "message": "MoMo API is running"})
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
