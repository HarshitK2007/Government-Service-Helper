import json
import os

FILE = "government_urls.json"

def load_urls():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_url(service, state, district):
    data = load_urls()

    return (
        data.get(service.lower().strip(), {})
            .get(state.lower().strip(), {})
            .get(district.lower().strip())
    )


def save_url(service, state, district, url):
    data = load_urls()


    service = service.lower().strip()
    state = state.lower().strip()
    district = district.lower().strip()

    data.setdefault(service, {})
    data[service].setdefault(state, {})

    data[service][state][district] = url

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
