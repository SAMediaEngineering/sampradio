import requests
from bs4 import BeautifulSoup
import datetime

SUPABASE_URL = "https://xmbqgdquikesysaspsdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYnFnZHF1aWtlc3lzYXNwc2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNDAzNjQsImV4cCI6MjA3MzkxNjM2NH0.MkPeVmG6pEonpgW01RuVP4xMZtWAer1qy3ASM5iye4Y"
TABLE = "Test123Airplay"

stations = {
    "Metro FM": "https://metrofm.co.za/nowplaying",
    "5FM": "https://5fm.co.za/nowplaying",
    "947": "https://www.947.co.za/nowplaying"
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
    response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE}", json=data, headers=headers)
    if response.status_code == 201:
        print(f"{station} - {song} inserted successfully")
    else:
        print(f"Failed to insert {station} - {song}: {response.text}")

def scrape_station(station_name, url, song_selector, artist_selector):
    try:
        # Bypass SSL verification for all stations
        response = requests.get(url, verify=False)
        
        soup = BeautifulSoup(response.text, "html.parser")
        song_element = soup.select_one(song_selector)
        artist_element = soup.select_one(artist_selector)
        if song_element and artist_element:
            insert_airplay(station_name, song_element.text.strip(), artist_element.text.strip(), url)
        else:
            print(f"No song/artist found for {station_name}")
    except Exception as e:
        print(f"Error scraping {station_name}: {e}")

# CSS selectors for each station (update if website changes)
scrape_station("Metro FM", "https://metrofm.co.za/nowplaying", ".now-playing-song", ".now-playing-artist")
scrape_station(
    "5FM",
    "http://listen.5fm.co.za/listen5fm/",
    ".td-player-bar__nowplaying__trackinfo__track-name span",  # update with real song selector
    "#td-player-bar__nowplaying__trackinfo__artist-name span"
)
scrape_station("947", "https://www.947.co.za/nowplaying", ".now-playing-song", ".now-playing-artist")
