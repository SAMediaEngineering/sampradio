import requests
from bs4 import BeautifulSoup

# KFM page on Radio South Africa
URL = "https://www.radio-south-africa.co.za/kfm"

try:
    response = requests.get(URL)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching KFM: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# --- Get current live song ---
current_song_tag = soup.select_one("#play-now-b")  # or #play-now-c
if current_song_tag:
    current_song = current_song_tag.text.strip()
    print(f"Current song: {current_song}")
else:
    print("No current song found")

# --- Get recent song history ---
history_songs = soup.select("#song_history .history-song")
songs_data = []

for song in history_songs:
    song_name_tag = song.select_one("span.song-name p")
    artist_tag = song.select_one("span.artist-name")
    timestamp_tag = song.select_one("span.time-stamp")
    link_tag = song.select_one("a")
    img_tag = song.select_one("img.lazy")

    song_info = {
        "song_name": song_name_tag.text.strip() if song_name_tag else None,
        "artist": artist_tag.text.strip() if artist_tag else None,
        "time": timestamp_tag.text.strip() if timestamp_tag else None,
        "link": link_tag['href'] if link_tag and link_tag.get('href') else None,
        "image": img_tag['src'] if img_tag and img_tag.get('src') else None
    }

    songs_data.append(song_info)

# Print all songs
for s in songs_data:
    print(s)
