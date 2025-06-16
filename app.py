from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import json
import os

DB_FILE = "momo.db"

def get_db_connection():
    """Get database connection with row factory for dictionary returns."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return dictionaries instead of tuples
    return conn

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})
    
    @app.route("/")
    def index():
        """Main index page."""
        return render_template("index.html")
    
    def load_transactions_from_json():
        """Load transactions from transactions.json file."""
        try:
            with open('transactions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("transactions.json not found")
            return []
        except json.JSONDecodeError:
            print("Error decoding transactions.json")
            return []
    
    @app.route("/api/transactions", methods=["GET"])
    def get_transactions():
        """Get all transactions with optional filtering."""
        try:
            # Get filter parameters
            tx_type = request.args.get('type')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            
            # Load transactions from JSON
            transactions = load_transactions_from_json()
            
            # Apply filters
            filtered_transactions = []
            for tx in transactions:
                # Convert tx_type to match the filter
                tx_type_match = tx.get('tx_type', '').lower() == (tx_type or '').lower()
                date_match = True
                
                if date_from or date_to:
                    tx_date = tx.get('tx_timestamp', '').split('T')[0]  # Get date part only
                    if date_from and tx_date < date_from:
                        date_match = False
                    if date_to and tx_date > date_to:
                        date_match = False
                
                if (not tx_type or tx_type_match) and date_match:
                    filtered_transactions.append(tx)
            
            return jsonify(filtered_transactions)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/transactions/volume", methods=["GET"])
    def get_transaction_volume():
        """Get transaction volume by type."""
        try:
            transactions = load_transactions_from_json()
            volume_by_type = {}
            
            for tx in transactions:
                tx_type = tx.get('tx_type', 'unknown')
                volume_by_type[tx_type] = volume_by_type.get(tx_type, 0) + 1
            
            return jsonify(volume_by_type)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/transactions/monthly", methods=["GET"])
    def get_monthly_transactions():
        """Get monthly transaction summary."""
        try:
            transactions = load_transactions_from_json()
            monthly_data = {}
            
            for tx in transactions:
                date = tx.get('tx_timestamp', '').split('T')[0][:7]  # Get YYYY-MM
                monthly_data[date] = monthly_data.get(date, 0) + 1
            
            return jsonify(monthly_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/transactions/distribution", methods=["GET"])
    def get_transaction_distribution():
        """Get transaction distribution between deposits and withdrawals."""
        try:
            transactions = load_transactions_from_json()
            deposits = 0
            withdrawals = 0
            
            for tx in transactions:
                amount = float(tx.get('amount', 0))
                tx_type = tx.get('tx_type', '').lower()
                
                if tx_type in ['deposit', 'incoming']:
                    deposits += amount
                elif tx_type in ['withdrawal', 'payment']:
                    withdrawals += abs(amount)
            
            return jsonify({
                "deposits": deposits,
                "withdrawals": withdrawals
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/transactions/top-types", methods=["GET"])
    def get_top_transaction_types():
        """Get top transaction types by volume."""
        try:
            transactions = load_transactions_from_json()
            type_counts = {}
            
            for tx in transactions:
                tx_type = tx.get('tx_type', 'unknown')
                type_counts[tx_type] = type_counts.get(tx_type, 0) + 1
            
            # Sort by count and get top 5
            top_types = dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5])
            return jsonify(top_types)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/summary", methods=["GET"])
    def get_summary():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total balance
        cursor.execute("SELECT SUM(amount) as total FROM transactions")
        total_balance = cursor.fetchone()["total"] or 0
        
        # Get transaction counts by type
        cursor.execute("""
            SELECT tx_type_id, COUNT(*) as count
            FROM transactions
            GROUP BY tx_type_id
        """)
        type_counts = [dict(row) for row in cursor.fetchall()]
        
        # Get recent transactions
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
    
    def init_db():
        """Initialize the database with required tables and data."""
        with app.app_context():
            db = get_db_connection()
            with app.open_resource('schema.sql') as f:
                db.executescript(f.read().decode('utf8'))
            
            # Initialize transaction types
            transaction_types = [
                ('incoming',),
                ('payment',),
                ('transfer',),
                ('deposit',),
                ('airtime',),
                ('cash_power',),
                ('withdrawal',),
                ('otp',)
            ]
            
            try:
                db.executemany('INSERT OR IGNORE INTO transaction_types (name) VALUES (?)', transaction_types)
                db.commit()
            except sqlite3.Error as e:
                print(f"Error initializing transaction types: {e}")
                db.rollback()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
