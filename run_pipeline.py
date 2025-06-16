from parse_momo_sms import parse_sms_file
from init_db import create_db
from insert_to_db import insert_transactions

def main():
    create_db()
    parsed_data = parse_sms_file('momo_sms.xml')  # replace with your file name
    insert_transactions(parsed_data)
    print(f"Inserted {len(parsed_data)} transactions into the database.")

if __name__ == "__main__":
    main()

