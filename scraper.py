import requests
from bs4 import BeautifulSoup
import datetime

# Supabase details
SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYnFnZHF1aWtlc3lzYXNwc2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNDAzNjQsImV4cCI6MjA3MzkxNjM2NH0.MkPeVmG6pEonpgW01RuVP4xMZtWAer1qy3ASM5iye4Y"
TABLE = "Test123Airplay"

# Stations and CSS selectors (update Metro FM selectors after inspecting page)
stations = {
    "5FM": {
        "url": "http://listen.5fm.co.za/listen5fm/",
        "song_selector": ".td-player-bar__nowplaying__trackinfo__track-name span",
        "artist_selector": "#td-player-bar__nowplaying__trackinfo__artist-name span"
    },
    "Metro FM": {
        "url": "https://www.metrofm.co.za/metro-fm/listen-live/",
        "song_selector": ".now-playing-song",    # placeholder
        "artist_selector": ".now-playing-artist" # placeholder
    }
}

def insert_airplay(station, song, artist, source_url):
    data = {
        "station_name": station,
        "song_title": song,
        "artist_name": artist,
        "play_time": datetime.datetime.utcnow().isoformat(),
        "source_url": source_url
    }
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE}", json=data, headers=headers)
        if response.status_code in [200, 201, 204]:
            print(f"{station} - {song} inserted successfully")
        else:
            print(f"Failed to insert {station} - {song}: {response.text}")
    except Exception as e:
        print(f"Error inserting into Supabase for {station}: {e}")

def scrape_station(station_name, config):
    try:
        response = requests.get(config["url"], verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        song_elem = soup.select_one(config["song_selector"])
        artist_elem = soup.select_one(config["artist_selector"])
        if song_elem and artist_elem:
            song = song_elem.text.strip()
            artist = artist_elem.text.strip()
            print(f"{station_name} is playing: {song} – {artist}")
            insert_airplay(station_name, song, artist, config["url"])
        else:
            print(f"No song/artist found for {station_name}")
    except Exception as e:
        print(f"Error scraping {station_name}: {e}")

def main():
    for station_name, config in stations.items():
        scrape_station(station_name, config)

if __name__ == "__main__":
    main()
