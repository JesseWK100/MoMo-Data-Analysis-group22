from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os
from functools import lru_cache
import time

# Cache the transactions data for 5 minutes
@lru_cache(maxsize=1)
def load_transactions_from_json():
    """Load transactions from transactions.json file with caching."""
    try:
        start_time = time.time()
        with open('transactions.json', 'r') as f:
            transactions = json.load(f)
        load_time = time.time() - start_time
        print(f"Loaded transactions in {load_time:.2f}s: {type(transactions)}, length: {len(transactions) if isinstance(transactions, list) else 'N/A'}")
        return transactions
    except FileNotFoundError:
        print("Error: transactions.json file not found")
        return []
    except json.JSONDecodeError:
        print("Error: transactions.json is not valid JSON")
        return []
    except Exception as e:
        print(f"Error loading transactions: {str(e)}")
        return []

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})
    
    # Clear the cache when the app starts
    load_transactions_from_json.cache_clear()
    
    @app.route("/")
    def index():
        """Main index page."""
        return render_template("index.html")
    
    @app.route("/api/transactions", methods=["GET"])
    def get_transactions():
        """Get all transactions with optional filtering."""
        try:
            start_time = time.time()
            # Get filter parameters
            tx_type = request.args.get('type')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            search = request.args.get('search', '').lower()

            # Load transactions from JSON (now cached)
            transactions = load_transactions_from_json()
            if not transactions:
                return jsonify([])

            # Apply filters
            filtered_transactions = []
            for tx in transactions:
                # Check search term in relevant fields
                search_match = True
                if search:
                    search_fields = [
                        str(tx.get('raw_body', '')),
                        str(tx.get('from_party', '')),
                        str(tx.get('to_party', '')),
                        str(tx.get('momo_tx_id', ''))
                    ]
                    search_match = any(search in field.lower() for field in search_fields)

                # Check transaction type
                tx_type_match = True
                if tx_type:
                    tx_type_match = tx.get('tx_type', '').lower() == tx_type.lower()

                # Check date range
                date_match = True
                if date_from or date_to:
                    tx_date = tx.get('tx_timestamp', '').split(' ')[0]  # Get date part only
                    if date_from and tx_date < date_from:
                        date_match = False
                    if date_to and tx_date > date_to:
                        date_match = False

                # Add transaction if all filters match
                if search_match and tx_type_match and date_match:
                    filtered_transactions.append(tx)

            process_time = time.time() - start_time
            print(f"Processed {len(filtered_transactions)} transactions in {process_time:.2f}s")
            return jsonify(filtered_transactions)

        except Exception as e:
            print(f"Error in get_transactions: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/transactions/volume", methods=["GET"])
    def get_transaction_volume():
        """Get transaction volume by type."""
        try:
            transactions = load_transactions_from_json()
            type_counts = {}
            for tx in transactions:
                tx_type = tx.get('tx_type', 'unknown')
                type_counts[tx_type] = type_counts.get(tx_type, 0) + 1
            return jsonify(type_counts)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/transactions/monthly", methods=["GET"])
    def get_monthly_transactions():
        """Get monthly transaction summary."""
        try:
            transactions = load_transactions_from_json()
            monthly_data = {}
            for tx in transactions:
                date = tx.get('tx_timestamp', '').split(' ')[0]
                month = date[:7]  # Get YYYY-MM
                monthly_data[month] = monthly_data.get(month, 0) + 1
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
                elif tx_type in ['withdrawal', 'payment', 'transfer']:
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
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "message": "MoMo API is running"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)