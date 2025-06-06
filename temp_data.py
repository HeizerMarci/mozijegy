import json
import os

TEMP_FILE = "temp_data.json"

def save_data(data):
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if not os.path.exists(TEMP_FILE):
        return {}
    with open(TEMP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clear_data():
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        f.write("{}")