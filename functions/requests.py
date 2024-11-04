import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.venv', '.env'))
vtex_api_key = os.getenv('VTEX_API_KEY')
vtex_api_token = os.getenv('VTEX_API_TOKEN')
price_endpoint = os.getenv('PRICE_ENDPOINT')

def vtex_get_prices(skus: list):
    json_path = os.path.join(os.path.dirname(__file__), '..', 'planilhas', 'vtex_response.json')
    headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'X-VTEX-API-AppKey': f"{vtex_api_key}",
    'X-VTEX-API-AppToken': f"{vtex_api_token}"
    }
    res = []
    for i, sku in enumerate(skus):

        if i > 0 and i % 30 == 0:
            time.sleep(1)

        req = requests.get(url=f'{price_endpoint}{sku}', headers=headers)
        try: 
            res.append([req.json()])
        except: continue
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        
    return json_path