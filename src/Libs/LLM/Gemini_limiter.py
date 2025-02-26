import json
import os
from datetime import datetime



output_folder = "src/.outputs"  
absolute_output_folder = os.path.join(os.getcwd(),output_folder,"_gemini_request_cache.json" )
print(absolute_output_folder)
CACHE_FILE = absolute_output_folder
REQUEST_LIMIT = 1000

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"date": str(datetime.today().date()), "count": 0}
    with open(CACHE_FILE, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {"date": str(datetime.today().date()), "count": 0}
    return data

def save_cache(data):
    with open(CACHE_FILE, "w") as file:
        json.dump(data, file)

def can_make_request():
    cache = load_cache()
    today = str(datetime.today().date())    
    if cache["date"] != today:
        cache = {"date": today, "count": 0}  # Reset count for a new day
        save_cache(cache)    
    return cache["count"] < REQUEST_LIMIT

def increment_request_count():
    cache = load_cache()
    print(f"Request count: {cache['count']}")
    cache["count"] += 1
    save_cache(cache)
