import xml.etree.ElementTree as ET
import re
from datetime import datetime

def parse_sms_file(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    messages = []

    for sms in root.findall('sms'):
        body = sms.find('body').text.strip()

        # Categorize and extract data
        parsed_data = categorize_and_extract(body)
        if parsed_data:
            messages.append(parsed_data)
        else:
            log_unrecognized(body)

    return messages

def categorize_and_extract(body):
    patterns = [
        # Incoming Money
        (r'received (\d+) RWF from ([\w\s]+).*Date: ([\d\-:\s]+)', 'Incoming Money'),
        # Payment to someone
        (r'payment of (\d+) RWF to ([\w\s]+).*Date: ([\d\-:\s]+)', 'Payment'),
        # Withdrawals
        (r'withdrawn (\d+) RWF.*on ([\d\-:\s]+)', 'Withdrawal'),
        # Internet Bundle
        (r'internet bundle.*?for (\d+) RWF.*', 'Internet Bundle'),
    ]

    for pattern, tx_type in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            if tx_type == "Withdrawal":
                amount, date = match.groups()
                return {
                    "type": tx_type,
                    "amount": int(amount),
                    "date": parse_date(date),
                    "raw_body": body
                }
            else:
                amount, receiver, date = match.groups()
                return {
                    "type": tx_type,
                    "amount": int(amount),
                    "receiver": receiver,
                    "date": parse_date(date),
                    "raw_body": body
                }

    return None

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except:
        return None

def log_unrecognized(body):
    with open('unprocessed_sms.txt', 'a') as f:
        f.write(body + '\n')
