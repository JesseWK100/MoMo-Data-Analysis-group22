#!/usr/bin/env python3
import re, json, logging
import xml.etree.ElementTree as ET
from datetime import datetime

# --- CONFIG ---
XML_FILE = 'modified_sms_v2.xml'
LOG_FILE = 'unprocessed.log'
# Patterns for each category
PATTERNS = {
    'incoming':     re.compile(r'received\s+([\d,]+)\s+RWF\s+from\s+(.+?)\s+\('),
    'payment':      re.compile(r'payment\s+of\s+([\d,]+)\s+RWF\s+to\s+(.+?)\s+(\d+)'),
    'transfer':     re.compile(r'(\d+)\s+RWF\s+transferred\s+to\s+(.+?)\s+\((\d+)\)\s+from\s+(\d+)\s+at\s+([\d\- :]+)\.\s+Fee\s+was:\s+(\d+)\s+RWF\.\s+New\s+balance:\s+(\d+)\s+RWF'),
    'deposit':      re.compile(r'A bank deposit of\s+([\d,]+)\s+RWF\s+has been added'),
    'airtime':      re.compile(r'payment of\s+([\d,]+)\s+RWF to Airtime'),
    'cash_power':   re.compile(r'payment of\s+([\d,]+)\s+RWF to MTN Cash Power'),
    'withdrawal':   re.compile(r'withdrawn\s+([\d,]+)\s+RWF\s+from.+?via agent:\s+(.+?)\s+\((\d+)\)'),
    'otp':          re.compile(r'one-time password is :(\d+)')
}

# --- SETUP LOGGING ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

def ms_to_dt(ms_str):
    """Convert UNIX-ms timestamp to datetime string."""
    dt = datetime.fromtimestamp(int(ms_str) / 1000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def parse_sms_element(elem):
    body = elem.get('body', '').strip()
    sms_id = f"{elem.get('protocol')}|{elem.get('address')}|{elem.get('date')}"
    ts = ms_to_dt(elem.get('date'))
    # try each pattern
    for name, pat in PATTERNS.items():
        m = pat.search(body)
        if m:
            data = {'sms_id': sms_id, 'raw_body': body, 'tx_type': name,
                    'tx_timestamp': ts, 'currency': 'RWF'}
            if name == 'incoming':
                data.update({
                    'amount': int(m.group(1).replace(',', '')),
                    'from_party': m.group(2).strip(),
                })
            elif name == 'payment':
                data.update({
                    'amount': int(m.group(1).replace(',', '')),
                    'to_party': m.group(2).strip(),
                    'momo_tx_id': m.group(3)
                })
            elif name == 'transfer':
                data.update({
                    'amount': int(m.group(1)),
                    'to_party': m.group(2).strip(),
                    'from_party': m.group(4),
                    'fee': int(m.group(6)),
                    'balance_after': int(m.group(7)),
                    'momo_tx_id': None
                })
            elif name == 'deposit':
                data.update({
                    'amount': int(m.group(1).replace(',', '')),
                })
            elif name in ('airtime','cash_power'):
                data.update({
                    'amount': int(m.group(1)),
                    'fee': 0
                })
            elif name == 'withdrawal':
                data.update({
                    'amount': int(m.group(1)),
                    'agent_id': m.group(3),
                    'from_party': elem.get('address')
                })
            elif name == 'otp':
                data.update({'extra_info': json.dumps({'otp': m.group(1)})})
            return data
    # if none matched
    logging.info(f"UNPROCESSED: {sms_id} | {body}")
    return None

def extract_all(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    out = []
    for sms in root.findall('sms'):
        rec = parse_sms_element(sms)
        if rec:
            out.append(rec)
    return out

if __name__ == '__main__':
    records = extract_all(XML_FILE)
    print(f"Extracted {len(records)} records out of ~1600 SMS.")
    # optionally: write to JSON for inspection
    import json
    with open('transactions.json', 'w') as f:
        json.dump(records, f, indent=2)
