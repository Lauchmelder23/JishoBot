import requests
import urllib.parse
import json

TEMPLATE_URL = "https://jisho.org/api/v1/search/words?keyword={0}"

def query(query: str):
    url = TEMPLATE_URL.format(urllib.parse.quote_plus(query))
    r = requests.get(url)

    if r.status_code != 200:
        print(f"ERROR: Failed to access Jisho API... {r.status_code}")
    
    return json.loads(r.text)