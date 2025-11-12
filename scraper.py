import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
import json
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYnFnZHF1aWtlc3lzYXNwc2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNDAzNjQsImV4cCI6MjA3MzkxNjM2NH0.MkPeVmG6pEonpgW01RuVP4xMZtWAer1qy3ASM5iye4Y"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
                    songs.append({
                        "station_name": "5FM",
                        "song_title": song.get("title", "Unknown Title"),
                        "artist_name": song.get("artist", "Unknown Artist"),
                        "play_time": datetime.fromtimestamp(song.get("timestamp", int(time.time() * 1000)) / 1000).isoformat(),
                        "created_at": datetime.utcnow().isoformat()
                    })
            except json.JSONDecodeError as e:
                print("Failed to decode songs JSON:", e)
            break
    return songs

def insert_new_songs_only(songs):
    if not songs:
        print("No songs to insert.")
        return

    new_songs = []
    for song in songs:
        # Check if this exact play already exists
        existing = supabase.table("Test123Airplay") \
            .select("id") \
            .eq("station_name", song["station_name"]) \
            .eq("song_title", song["song_title"]) \
            .eq("artist_name", song["artist_name"]) \
            .eq("play_time", song["play_time"]) \
            .execute()

        if not existing.data or len(existing.data) == 0:
            new_songs.append(song)  # Only append if not already in DB

    if new_songs:
        supabase.table("Test123Airplay").insert(new_songs).execute()
        print(f"Inserted {len(new_songs)} new songs.")
    else:
        print("No new songs to insert; all fetched songs already exist.")

if __name__ == "__main__":
    songs = fetch_5fm_history()
    insert_new_songs_only(songs)
