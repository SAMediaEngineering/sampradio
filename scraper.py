import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
import json
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYnFnZHF1aWtlc3lzYXNwc2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNDAzNjQsImV4cCI6MjA3MzkxNjM2NH0.MkPeVmG6pEonpgW01RuVP4xMZtWAer1qy3ASM5iye4Y"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STATIONS TO SCRAPE ---
STATIONS = {
    "5FM": "https://player.listenlive.co/71331/en/songhistory",
    "947": "https://player.listenlive.co/45771/en/songhistory",
    "KFM 94.5": "https://player.listenlive.co/45781/en/songhistory",
    "RSG": "https://player.listenlive.co/71471/en/songhistory",
}

# --- FETCH SONGS FOR A GIVEN STATION ---
def fetch_station_history(station_name, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.118 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {station_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    songs = []

    for script in soup.find_all("script"):
        if "var songs =" in script.text:
            start = script.text.find("var songs =") + len("var songs =")
            end = script.text.find("];", start) + 1
            songs_json = script.text[start:end].strip()
            try:
                songs_list = json.loads(songs_json)
                for song in songs_list:
                    songs.append({
                        "station_name": station_name,
                        "song_title": song.get("title", "Unknown Title"),
                        "artist_name": song.get("artist", "Unknown Artist"),
                        "play_time": datetime.fromtimestamp(
                            song.get("timestamp", int(time.time() * 1000)) / 1000
                        ).isoformat(),
                        "created_at": datetime.utcnow().isoformat()
                    })
            except json.JSONDecodeError:
                print(f"Failed to decode songs JSON for {station_name}")
            break

    print(f"Fetched {len(songs)} songs from {station_name}")
    return songs

# --- INSERT NEW SONGS INTO SUPABASE ---
def insert_to_supabase(all_songs):
    if not all_songs:
        print("No songs found to insert.")
        return

    # Fetch all existing records
    existing = supabase.table("Test123Airplay").select(
        "station_name,song_title,artist_name,play_time"
    ).execute()

    existing_set = set()
    if existing.data:
        existing_set = set(
            (row["station_name"], row["song_title"], row["artist_name"], row["play_time"])
            for row in existing.data
        )

    new_songs = [
        song for song in all_songs
        if (song["station_name"], song["song_title"], song["artist_name"], song["play_time"]) not in existing_set
    ]

    if not new_songs:
        print("No new songs to insert — all already exist.")
        return

    res = supabase.table("Test123Airplay").insert(new_songs).execute()
    if res.data:
        print(f"✅ Inserted {len(new_songs)} new songs:")
        for song in new_songs:
            print(f"  - {song['station_name']}: {song['song_title']} – {song['artist_name']}")
    else:
        print(f"❌ Failed to insert. Response: {res.data}")

# --- MAIN ---
if __name__ == "__main__":
    all_songs = []
    for name, url in STATIONS.items():
        all_songs.extend(fetch_station_history(name, url))
    insert_to_supabase(all_songs)
