import json
import os
import time

CACHE_FILE = "go2web_cache.json"
CACHE_TTL = 300

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_cache_entry(url):
    cache = load_cache()
    if url in cache:
        entry = cache[url]
        return entry
    return None

def get_from_cache(url):
    entry = get_cache_entry(url)
    if entry:
        age = time.time() - entry["timestamp"]
        if age < CACHE_TTL:
            print(f"Serving from cache ({int(CACHE_TTL - age)}s remaining)")
            return entry["status_line"], entry["headers"], entry["body"]
    return None

def get_conditional_headers(url):
    entry = get_cache_entry(url)
    if not entry:
        return ""

    headers = ""
    if "etag" in entry:
        headers += f"If-None-Match: {entry['etag']}\r\n"
    if "last_modified" in entry:
        headers += f"If-Modified-Since: {entry['last_modified']}\r\n"
    return headers

def store_in_cache(url, status_line, headers, body):
    cache = load_cache()
    entry = {
        "status_line": status_line,
        "headers": headers,
        "body": body,
        "timestamp": time.time()
    }

    for header in headers:
        lower = header.lower()
        if lower.startswith("etag:"):
            entry["etag"] = header.split(": ", 1)[1].strip()
        elif lower.startswith("last-modified:"):
            entry["last_modified"] = header.split(": ", 1)[1].strip()

    cache[url] = entry
    save_cache(cache)