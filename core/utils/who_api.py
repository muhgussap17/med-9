# core/utils/who_api.py

import requests
from functools import lru_cache

WHO_TOKEN_URL = "https://icdaccessmanagement.who.int/connect/token"
WHO_SEARCH_URL = "https://id.who.int/icd/release/11/2023-01/mms/search"

CLIENT_ID = 'bd6b7a5f-4d65-4954-8f3d-f1f253246a11_807fc733-bca0-4305-80e1-a84cc9ff013d'
CLIENT_SECRET = 'HnZV3GiXnG3ropAlag4Pt/YpHxAk50FL0MlF7b32WCo='

@lru_cache(maxsize=1)
def get_who_token():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'icdapi_access'
    }

    res = requests.post(WHO_TOKEN_URL, data=payload, verify=False)
    if res.status_code == 200:
        return res.json().get('access_token')
    return None


def search_icd(query):
    token = get_who_token()
    if not token:
        return []

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json; charset=utf-8',
        'Accept-Language': 'en',
        'API-Version': 'v2'
    }

    params = {
        'q': query,
        'useFlexisearch': 'true',
        'linearization': 'mms'
    }

    res = requests.get(WHO_SEARCH_URL, headers=headers, params=params, verify=False)
    if res.status_code == 200:
        entities = res.json().get('destinationEntities', [])

        results = []
        for entity in entities:
            raw_title = entity.get("title", "")
            cleaned_title = raw_title.replace("<em class='found'>", "").replace("</em>", "")
            code = entity.get("code", None)  # ← ini hanya ada jika WHO API menyediakannya

            # Cek jika ada kode ICD (kalau tidak, bisa fallback ke ID terakhir URL-nya)
            if not code:
                # Ambil ID dari URI terakhir
                full_id = entity.get("id", "")
                code = full_id.split("/")[-1] if full_id else "UnknownCode"

            formatted_value = f"{code} - {cleaned_title}"
            results.append({
                "id": formatted_value,
                "text": formatted_value
            })

        return results
    
    return []
