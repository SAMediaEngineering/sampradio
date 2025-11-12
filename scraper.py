import requests
import json
import re

def fetch_5fm_history_js():
    url = "https://player.listenlive.co/71331/en/songhistory"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.118 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching 5FM page:", e)
        return

    # Extract the 'songs' JSON from the script tag
    match = re.search(r"var songs = (\[.*?\]);", response.text, re.DOTALL)
    if not match:
        print("Could not find songs data in page.")
        return

    try:
        songs = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print("Failed to parse songs JSON:", e)
        return

    print("Last songs played on 5FM:\n")
    for s in songs:
        title = s.get("title", "Unknown Title")
        artist = s.get("artist", "Unknown Artist")
        print(f"{title} – {artist}")

if __name__ == "__main__":
    fetch_5fm_history_js()
