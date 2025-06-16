import json
from pathlib import Path

def get_transactions():
    try:
        # Get the absolute path to the transactions.json file
        json_path = Path(__file__).parent / 'transactions.json'
        
        # Check if file exists
        if not json_path.exists():
            raise FileNotFoundError(f"Transactions file not found at {json_path}")
            
        # Read and parse the JSON file
        with open(json_path, 'r') as f:
            transactions = json.load(f)
            
        return transactions
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise 