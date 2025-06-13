def format_transaction_row(row):
    return {
        "id": row["id"],
        "type": row["type"],
        "receiver": row["receiver"],
        "amount": row["amount"],
        "date": row["date"],
        "raw_body": row["raw_body"]
    }

