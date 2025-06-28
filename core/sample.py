import requests

# Token API WHO
token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
client_id = 'bd6b7a5f-4d65-4954-8f3d-f1f253246a11_807fc733-bca0-4305-80e1-a84cc9ff013d'
client_secret = 'HnZV3GiXnG3ropAlag4Pt/YpHxAk50FL0MlF7b32WCo='

payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'icdapi_access'
}

response = requests.post(token_endpoint, data=payload, verify=False)
token = response.json().get('access_token')
print("Token:", token)

# STEP 2 - Cari ICD
search_url = 'https://id.who.int/icd/release/11/2023-01/mms/search'
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json; charset=utf-8',
    'Accept-Language': 'en',
    'API-Version': 'v2'
}

params = {
    'q': 'diabetes',
    'useFlexisearch': 'true',
    'linearization': 'mms'
}

search_response = requests.get(search_url, headers=headers, params=params, verify=False)
print("Status:", search_response.status_code)
print("Hasil:")
print(search_response.json())
