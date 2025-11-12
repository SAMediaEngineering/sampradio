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

    # Extract songs JSON from <script>
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
                        "play_time": datetime.fromtimestamp(song.get("timestamp", int(time.time() * 1000)) / 1000),
                        "created_at": datetime.utcnow()
                    })
            except json.JSONDecodeError as e:
                print("Failed to decode songs JSON:", e)
            break
    return songs

def insert_to_supabase(songs):
    if not songs:
        print("No songs to insert.")
        return
    for song in songs:
        res = supabase.table("Test123Airplay").insert(song).execute()
        if res.status_code == 201:
            print(f"Inserted: {song['song_title']} – {song['artist_name']}")
        else:
            print(f"Failed to insert: {song}, Response: {res.data}")

if __name__ == "__main__":
    songs = fetch_5fm_history()
    insert_to_supabase(songs)
