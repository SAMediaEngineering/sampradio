import requests

def fetch_5fm_history():
    url = "https://player.listenlive.co/71331/en/songhistory"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise an error if request failed
    except requests.RequestException as e:
        print("Error fetching 5FM history:", e)
        return

    data = response.json()
    songs = data.get('songs', [])
    
    if not songs:
        print("No song/artist currently found for 5FM")
        return

    print("Last songs played on 5FM:\n")
    for s in songs:
        title = s.get('title', 'Unknown Title')
        artist = s.get('artist', 'Unknown Artist')
        print(f"{title} – {artist}")

if __name__ == "__main__":
    fetch_5fm_history()
