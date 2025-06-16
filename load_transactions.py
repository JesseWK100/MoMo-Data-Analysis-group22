import requests

def load_transactions():
    response = requests.post('http://127.0.0.1:5000/api/load-transactions')
    print(response.json())

if __name__ == '__main__':
    load_transactions() 