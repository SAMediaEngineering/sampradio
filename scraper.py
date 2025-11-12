import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYnFnZHF1aWtlc3lzYXNwc2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNDAzNjQsImV4cCI6MjA3MzkxNjM2NH0.MkPeVmG6pEonpgW01RuVP4xMZtWAer1qy3ASM5iye4Y"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# KFM live page
URL = "https://www.radio-south-africa.co.za/kfm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

songs_data = []

# Grab the current live song
current_song_div = soup.select_one(".current-song, .live-song")
if current_song_div:
    song_name = current_song_div.find("p")
    artist_name = current_song_div.find("span", class_="artist-name")
    song_info = {
        "song_name": song_name.text.strip() if song_name else None,
        "artist": artist_name.text.strip() if artist_name else None,
        "time": "LIVE",
        "link": None,
        "image": None
    }
    songs_data.append(song_info)

# Grab previous songs
history_songs = soup.select(".history-song")
for hs in history_songs:
    song_name_el = hs.find("span", class_="song-name")
    artist_name_el = hs.find("span", class_="artist-name")
    timestamp_el = hs.find("span", class_="time-stamp")
    link_el = hs.find("a", href=True)
    image_el = hs.find("img", src=True)

    song_info = {
        "song_name": song_name_el.get_text(strip=True) if song_name_el else None,
        "artist": artist_name_el.get_text(strip=True) if artist_name_el else None,
        "time": timestamp_el.get_text(strip=True) if timestamp_el else None,
        "link": link_el["href"] if link_el else None,
        "image": image_el["src"] if image_el else None
    }
    songs_data.append(song_info)

# Insert into Supabase table (table name: 'kfm_songs')
for song in songs_data:
    supabase.table("kfm_songs").upsert(song).execute()

print(f"Inserted {len(songs_data)} songs into Supabase.")
