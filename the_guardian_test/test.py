import requests
import json

API_KEY = "93a0c28f-66b8-49fe-834d-dd0e2a325a6c"
BASE_URL = "https://content.guardianapis.com/search"
JSON_FILE = "guardian_metadata_output/2026-06.json"

def fetch_and_save_json():
    params = {
        "q": "NASDAQ",
        "api-key": API_KEY,
        "from-date": "2026-06-01",
        "to-date": "2026-06-30",
        "show-fields": "bodyText",
        "show-tags": "all",
        "show-section": "true"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    metadata_list = []

    for item in data["response"]["results"]:
        metadata_list.append({
            "title": item.get("webTitle"),
            "link": item.get("webUrl"),
            "section": item.get("sectionName"),
            "bodyText": item.get("fields", {}).get("bodyText"),
        })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

    print(f"已儲存到 {JSON_FILE}")

def load_json():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 第一次執行時先抓資料並存檔
fetch_and_save_json()

'''
# 之後可直接讀 JSON
data = load_json()
for item in data[:3]:
    print("標題:", item.get("title"))
    print("連結:", item.get("link"))
    print("版面:", item.get("section"))
    print("內文:", item.get("bodyText"))
    print()
'''