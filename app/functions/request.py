import requests

r = requests.get('http://localhost:2480/database/test_db/select%20from%20created', auth=('root', 'don1664'))

print r.status_code
print r.headers['content-type']
print r.json()