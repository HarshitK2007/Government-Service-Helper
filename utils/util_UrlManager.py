import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(BASE_DIR, "data", "government_urls.json")

def load_urls():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()
        return json.loads(content) if content else {}

def get_url(need, state, dist):
    data = load_urls()
    try:
        lookup_key = f"{need}-{state}-{dist}"
        return data[lookup_key]
    except:
        return None


def save_url(need, state, dist, url):
    data = load_urls()

    need = need.lower().strip()
    state = state.lower().strip()
    dist = dist.lower().strip()

    data[f"{need}-{state}-{dist}"] = url

    os.makedirs(os.path.dirname(FILE), exist_ok=True)

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
