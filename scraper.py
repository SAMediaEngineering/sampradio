import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
import json
from datetime import datetime, timedelta

# Supabase credentials
SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "YOUR_ANON_KEY"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# How far back to check for duplicates
DUPLICATE_CHECK_HOURS = 24

def fetch_5fm_history():
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
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    songs = []

    scripts = soup.find_all("script")
    for s in scripts:
        if "var songs =" in s.text:
            start = s.text.find("var songs =") + len("var songs =")
            end = s.text.find("];", start) + 1
            songs_json = s.text[start:end].strip()
            try:
                songs_list = json.loads(songs_json)
                for song in songs_list:
                    play_time = datetime.fromtimestamp(
                        song.get("timestamp", int(time.time() * 1000)) / 1000
                    )
                    songs.append({
                        "station_name": "5FM",
                        "song_title": song.get("title", "Unknown Title"),
                        "artist_name": song.get("artist", "Unknown Artist"),
                        "play_time": play_time.isoformat(),
                        "created_at": datetime.utcnow().isoformat()
                    })
            except json.JSONDecodeError as e:
                print("Failed to decode songs JSON:", e)
            break
    return songs

def insert_to_supabase(songs):
    if not songs:
        print("No songs to insert.")
        return

    # Define cutoff time for duplicates
    cutoff_time = datetime.utcnow() - timedelta(hours=DUPLICATE_CHECK_HOURS)
    cutoff_iso = cutoff_time.isoformat()

    # Fetch recent songs from Supabase to avoid duplicates
    recent_songs = supabase.table("Test123Airplay") \
        .select("song_title, artist_name, play_time") \
        .gte("play_time", cutoff_iso) \
        .execute()

    existing = {(row["song_title"], row["artist_name"], row["play_time"]) for row in recent_songs.data}

    # Filter new songs
    new_songs = [
        song for song in songs
        if (song["song_title"], song["artist_name"], song["play_time"]) not in existing
    ]

    if not new_songs:
        print("No new songs to insert.")
        return

    # Bulk insert new songs
    res = supabase.table("Test123Airplay").insert(new_songs).execute()
    print(f"Inserted {len(new_songs)} new songs.")

if __name__ == "__main__":
    songs = fetch_5fm_history()
    insert_to_supabase(songs)
