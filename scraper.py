import requests
from bs4 import BeautifulSoup

url_5fm = "http://listen.5fm.co.za/listen5fm/"

try:
    # Fetch the page (ignore SSL for now)
    response = requests.get(url_5fm, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find artist and song
    artist_tag = soup.select_one("#td-player-bar__nowplaying__trackinfo__artist-name span")
    song_tag = soup.select_one("#td-player-bar__nowplaying__trackinfo__cue-title span")

    if artist_tag and song_tag:
        artist = artist_tag.text.strip()
        song = song_tag.text.strip()
        print(f"5FM Now Playing: {artist} - {song}")
    else:
        print("No song/artist currently found for 5FM")

except Exception as e:
    print(f"Error scraping 5FM: {e}")
