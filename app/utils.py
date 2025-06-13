def format_transaction_row(row):
    return {
        "id": row["sms_id"],
        "type": row["type_name"],
        "receiver": row["to_party"] or row["from_party"],
        "amount": row["amount"],
        "date": row["tx_timestamp"],
        "raw_body": row["raw_body"]
    }

